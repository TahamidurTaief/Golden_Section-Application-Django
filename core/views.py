from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
import json

from categories.models import Category, SubCategory
from services.models import Service
from providers.models import Provider
from content.models import Testimonial, BlogPost


def home(request):
    """Home page with featured content"""
    context = {
        'featured_categories': Category.objects.filter(is_featured=True, is_active=True)[:6],
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_providers': Provider.objects.filter(is_active=True).count(),
        'total_customers': 1000,  # Can be calculated from service requests
        'featured_services': Service.objects.filter(is_featured=True, is_active=True)[:6],

    }
    return render(request, 'home.html', context)


def home_content(request):
    """Return home page content for HTMX lazy loading"""
    context = {
        'featured_categories': Category.objects.filter(is_featured=True, is_active=True)[:6],
        'popular_services': Service.objects.filter(is_popular=True, is_active=True)[:8],
        'popular_providers': Provider.objects.filter(is_featured=True, is_active=True)[:4],
        'testimonials': Testimonial.objects.filter(is_featured=True, is_active=True)[:6],
        'blog_posts': BlogPost.objects.filter(is_published=True)[:3],
    }
    return render(request, 'components/home/home_content_partial.html', context)


def services(request):
    # Get filter parameters
    keyword = request.GET.get('keyword', '')
    categories = request.GET.getlist('category')
    subcategories = request.GET.getlist('subcategory')
    page = request.GET.get('page', 1)
    
    # Start with all active services
    services_qs = Service.objects.filter(is_active=True).select_related('category', 'subcategory')
    
    # Apply keyword search
    if keyword:
        services_qs = services_qs.filter(
            models.Q(name__icontains=keyword) |
            models.Q(short_description__icontains=keyword) |
            models.Q(description__icontains=keyword)
        )
    
    # Apply category filter
    if categories and 'all' not in categories:
        services_qs = services_qs.filter(category__slug__in=categories)
    
    # Apply subcategory filter
    if subcategories and 'all' not in subcategories:
        services_qs = services_qs.filter(subcategory__slug__in=subcategories)
    
    # Pagination
    paginator = Paginator(services_qs, 10)  # 10 services per page
    try:
        services_page = paginator.page(page)
    except PageNotAnInteger:
        services_page = paginator.page(1)
    except EmptyPage:
        services_page = paginator.page(paginator.num_pages)
    
    context = {
        'services': services_page,
        'services_count': paginator.count,
        'all_categories': Category.objects.filter(is_active=True),
        'all_subcategories': SubCategory.objects.filter(is_active=True),
        'paginator': paginator,
        'page_obj': services_page,
    }
    
    # If it's an HTMX request, return only the services list with pagination
    if request.headers.get('HX-Request'):
        return render(request, 'components/services/services_with_pagination.html', context)
    
    return render(request, 'services.html', context)


def search_categories(request):
    """Search categories based on query"""
    search_query = request.POST.get('category-search', '').lower()
    
    # Get categories from database
    categories_qs = Category.objects.filter(is_active=True)
    
    # Filter categories based on search
    if search_query:
        categories_qs = categories_qs.filter(name__icontains=search_query)
    
    context = {
        'categories': categories_qs,
        'show_all': True,
    }
    
    return render(request, 'components/services/category_list_partial.html', context)


def search_subcategories(request):
    """Search subcategories based on query"""
    search_query = request.POST.get('subcategory-search', '').lower()
    
    # Get subcategories from database
    subcategories_qs = SubCategory.objects.filter(is_active=True)
    
    # Filter subcategories based on search
    if search_query:
        subcategories_qs = subcategories_qs.filter(name__icontains=search_query)
    
    context = {
        'subcategories': subcategories_qs,
        'show_all': True,
    }
    
    return render(request, 'components/services/subcategory_list_partial.html', context)


def service_details(request, pk):
    """
    Service details view with all related data:
    - Service with category/subcategory
    - Provider information
    - Additional images for gallery
    - Sub-services
    - Service includes
    - FAQs
    - Business hours
    """
    service = get_object_or_404(
        Service.objects.select_related(
            'category', 
            'subcategory', 
            'provider'
        ).prefetch_related(
            'additional_images',
            'sub_services',
            'includes',
            'faqs',
            'business_hours'
        ),
        pk=pk
    )
    
    # Increment views count
    service.increment_views()
    
    context = {
        'service': service,
        'additional_images': service.additional_images.all(),
        'sub_services': service.sub_services.all(),
        'includes': service.includes.all(),
        'faqs': service.faqs.all(),
        'business_hours': service.business_hours.all().order_by('weekday'),
    }
    return render(request, 'service_details.html', context)


def booking(request, service_id):
    """Handle booking page with service details"""
    import json
    
    # Fetch service data by ID
    service = get_object_or_404(
        Service.objects.select_related('provider', 'category', 'subcategory')
        .prefetch_related('sub_services', 'includes', 'faqs', 'additional_images'),
        id=service_id
    )
    
    provider = service.provider
    sub_services_list = list(service.sub_services.all())
    
    # Initialize context with service data
    context = {
        'service': service,
        'provider': provider,
        'service_name': service.name,
        'provider_name': provider.business_name if provider else '',
        'all_sub_services': sub_services_list,
        'selected_sub_services': [],
        'location_latitude': '',
        'location_longitude': '',
        'location_address': '',
        'from_service_details': True
    }
    
    # If POST request, get additional data from form
    if request.method == 'POST':
        selected_sub_services_json = request.POST.get('selected_sub_services')
        location_latitude = request.POST.get('location_latitude')
        location_longitude = request.POST.get('location_longitude')
        location_address = request.POST.get('location_address')
        
        # Debug: Print received data
        print("=" * 50)
        print("Booking POST Data Received:")
        print(f"Service ID: {service_id}")
        print(f"Service Name: {service.name}")
        print(f"Provider: {provider.business_name if provider else 'N/A'}")
        print(f"Location: {location_address}")
        print(f"Coordinates: {location_latitude}, {location_longitude}")
        print(f"Sub-services JSON: {selected_sub_services_json}")
        print("=" * 50)
        
        # Parse selected sub-services
        try:
            selected_sub_services = json.loads(selected_sub_services_json) if selected_sub_services_json else []
            print(f"Parsed sub-services: {selected_sub_services}")
        except Exception as e:
            print(f"Error parsing sub-services: {e}")
            selected_sub_services = []
        
        # Update context with POST data
        context.update({
            'selected_sub_services': selected_sub_services,
            'location_latitude': location_latitude,
            'location_longitude': location_longitude,
            'location_address': location_address,
        })
    
    return render(request, 'booking.html', context)

def service_request(request):
    """Handle service request page with multi-step form"""
    if request.method == 'POST':
        # Handle form submission steps via HTMX
        step = request.POST.get('step')
        
        if step == 'basic_info':
            # Validate basic information step
            required_fields = ['firstName', 'lastName', 'email', 'phone', 'bookingEstimate']
            form_data = {field: request.POST.get(field, '') for field in required_fields}
            
            # Simple validation
            errors = []
            for field in required_fields:
                if not form_data[field]:
                    errors.append(f'{field} is required')
            
            if errors:
                return JsonResponse({'success': False, 'errors': errors})
            
            # Store in session for multi-step form
            request.session['service_request_data'] = request.session.get('service_request_data', {})
            request.session['service_request_data'].update(form_data)
            request.session['service_request_data']['ccZone'] = bool(request.POST.get('ccZone'))
            
            return JsonResponse({'success': True, 'next_step': 'booking_schedule'})
            
        elif step == 'booking_schedule':
            # Validate booking schedule step
            form_data = {
                'bookingDateTime': request.POST.get('bookingDateTime', ''),
                'numberOfPeople': request.POST.get('numberOfPeople', '1'),
                'hourlyRate': request.POST.get('hourlyRate', '70'),
                'sameNumberAllVans': bool(request.POST.get('sameNumberAllVans'))
            }
            
            request.session['service_request_data'].update(form_data)
            return JsonResponse({'success': True, 'next_step': 'collection_address'})
            
        elif step == 'collection_address':
            # Validate collection address step
            required_fields = ['collectionAddress', 'collectionPostalCode', 'collectionCity', 
                             'collectionPropertyType', 'collectionFloorLevel']
            form_data = {field: request.POST.get(field, '') for field in required_fields}
            
            form_data.update({
                'collectionBedrooms': request.POST.get('collectionBedrooms', '1'),
                'collectionHasLift': bool(request.POST.get('collectionHasLift'))
            })
            
            request.session['service_request_data'].update(form_data)
            return JsonResponse({'success': True, 'next_step': 'delivery_address'})
            
        elif step == 'delivery_address':
            # Validate delivery address step
            required_fields = ['deliveryAddress', 'deliveryPostalCode', 'deliveryCity', 
                             'deliveryPropertyType', 'deliveryFloorLevel']
            form_data = {field: request.POST.get(field, '') for field in required_fields}
            
            form_data.update({
                'deliveryBedrooms': request.POST.get('deliveryBedrooms', '1'),
                'deliveryHasLift': bool(request.POST.get('deliveryHasLift')),
                'sameAsCollection': bool(request.POST.get('sameAsCollection'))
            })
            
            request.session['service_request_data'].update(form_data)
            return JsonResponse({'success': True, 'next_step': 'additional_items'})
            
        elif step == 'additional_items':
            # Handle additional items step
            form_data = {
                'additionalNotes': request.POST.get('additionalNotes', '')
            }
            
            request.session['service_request_data'].update(form_data)
            return JsonResponse({'success': True, 'next_step': 'review_order'})
            
        elif step == 'submit_quote':
            # Final submission - could save to database here
            service_data = request.session.get('service_request_data', {})
            
            # Here you could:
            # 1. Save to database
            # 2. Send email notifications
            # 3. Generate quote reference number
            
            # For now, just return success
            return JsonResponse({
                'success': True, 
                'message': 'Quote request submitted successfully!',
                'whatsapp_redirect': True
            })
    
    # GET request - render the main template
    context = {
        'service_request_data': request.session.get('service_request_data', {})
    }
    return render(request, 'service_request.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def service_request_step(request):
    """Handle HTMX form step submissions"""
    try:
        data = json.loads(request.body)
        step = data.get('step')
        form_data = data.get('formData', {})
        
        # Store form data in session
        if 'service_request_data' not in request.session:
            request.session['service_request_data'] = {}
        
        request.session['service_request_data'].update(form_data)
        request.session.modified = True
        
        return JsonResponse({'success': True, 'step': step})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_service_request_data(request):
    """Get stored service request data for review"""
    data = request.session.get('service_request_data', {})
    return JsonResponse({'data': data})


def categories(request):
    return render(request, 'categories.html')