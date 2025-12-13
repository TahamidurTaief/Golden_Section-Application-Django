from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
import json

from services.models import Service
from .models import ServiceRequest
from .utils import send_whatsapp_quotation, get_whatsapp_quotation_url


@require_http_methods(["POST"])
def create_service_request(request):
    """Create a new service request/quotation"""
    try:
        # Check if multipart form data (file upload)
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = request.POST
            files = request.FILES
        elif request.content_type == 'application/json':
            data = json.loads(request.body)
            files = None
        else:
            data = request.POST
            files = request.FILES if hasattr(request, 'FILES') else None
        
        print("=" * 60)
        print("NEW SERVICE REQUEST RECEIVED")
        print("=" * 60)
        print(f"Content-Type: {request.content_type}")
        print(f"Request Method: {request.method}")
        print(f"Data received: {dict(data)}")
        if files:
            print(f"Files received: {list(files.keys())}")
        print("=" * 60)
        
        # Validate required fields
        required_fields = [
            'service_id', 'first_name', 'last_name', 'email', 'phone'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
        
        # Get service
        service = get_object_or_404(Service, id=data['service_id'])
        
        # Parse booking date and time separately
        booking_date_str = data.get('booking_date', '')
        booking_time_str = data.get('booking_time', '')
        booking_datetime = None
        booking_date = None
        booking_time = None
        
        if booking_date_str and booking_time_str:
            # Combine date and time
            try:
                # Parse date (YYYY-MM-DD)
                booking_date = datetime.strptime(booking_date_str, '%Y-%m-%d').date()
                
                # Parse time (HH:MM AM/PM) - store as string
                booking_time = booking_time_str.strip()
                
                # Combine into datetime for booking_datetime field
                time_obj = datetime.strptime(booking_time_str, '%I:%M %p').time()
                booking_datetime = datetime.combine(booking_date, time_obj)
                booking_datetime = timezone.make_aware(booking_datetime, timezone.get_current_timezone())
            except ValueError as e:
                print(f"Date/Time parsing error: {e}")
                booking_datetime = None
                booking_date = None
                booking_time = None
        
        # Parse location
        location_address = data.get('location_address', '').strip()
        location_latitude = data.get('location_latitude', None)
        location_longitude = data.get('location_longitude', None)
        
        # Convert string 'null' or empty to None for coordinates
        if location_latitude in ['null', '', None]:
            location_latitude = None
        if location_longitude in ['null', '', None]:
            location_longitude = None
        
        # Parse numeric fields - these are optional now
        try:
            number_of_people = int(data.get('number_of_people', 1)) if data.get('number_of_people') else 1
            hourly_rate = float(data.get('hourly_rate', 0)) if data.get('hourly_rate') else None
        except (ValueError, TypeError) as e:
            number_of_people = 1
            hourly_rate = None
            print(f"Warning - numeric field parsing: {str(e)}")
        
        # Create service request
        service_request = ServiceRequest.objects.create(
            service=service,
            first_name=data['first_name'].strip(),
            last_name=data['last_name'].strip(),
            email=data['email'].strip().lower(),
            phone=data['phone'].strip(),
            pricing_tier=data.get('pricing_tier', '').strip(),
            booking_estimate=data.get('booking_estimate', '').strip(),
            booking_date=booking_date,
            booking_time=booking_time,  # Now stored as string
            booking_datetime=booking_datetime,
            number_of_people=number_of_people,
            hourly_rate=hourly_rate,
            location_address=location_address,
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            additional_notes=data.get('additional_notes', '').strip(),
            cc_zone=data.get('cc_zone', 'false').lower() == 'true' if isinstance(data.get('cc_zone'), str) else bool(data.get('cc_zone', False))
        )
        
        print(f"ServiceRequest created successfully: ID={service_request.id}, Customer={service_request.customer_name}")
        
        # Handle file uploads
        if files:
            from .models import RequestAttachment
            for file_key in files:
                for uploaded_file in files.getlist(file_key):
                    # Determine file type
                    file_type = 'document'
                    if uploaded_file.content_type.startswith('image/'):
                        file_type = 'image'
                    elif uploaded_file.content_type.startswith('video/'):
                        file_type = 'video'
                    
                    # Create attachment
                    RequestAttachment.objects.create(
                        request=service_request,
                        file=uploaded_file,
                        file_type=file_type,
                        file_name=uploaded_file.name,
                        file_size=uploaded_file.size
                    )
                    print(f"File uploaded: {uploaded_file.name} ({file_type})")
        
        print(f"ServiceRequest created successfully: ID={service_request.id}, Customer={service_request.customer_name}")
        
        # Send WhatsApp notification automatically
        try:
            whatsapp_sent = send_whatsapp_quotation(service_request)
        except Exception as e:
            print(f"WhatsApp notification failed for request {service_request.id}: {str(e)}")
            whatsapp_sent = False
        
        # Generate WhatsApp URL
        try:
            whatsapp_url = get_whatsapp_quotation_url(service_request)
        except Exception as e:
            print(f"WhatsApp URL generation failed for request {service_request.id}: {str(e)}")
            whatsapp_url = None
        
        return JsonResponse({
            'success': True,
            'request_id': service_request.id,
            'message': 'Service request submitted successfully!',
            'whatsapp_sent': whatsapp_sent,
            'whatsapp_url': whatsapp_url,
            'request_details': {
                'id': service_request.id,
                'customer_name': service_request.customer_name,
                'service_name': service_request.service.name,
                'booking_date': booking_date.strftime('%B %d, %Y') if booking_date else 'Not specified',
                'booking_time': booking_time or 'Not specified',
                'location': location_address or 'Not specified',
                'status': service_request.get_status_display()
            }
        })
        
    except Service.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Service not found'
        }, status=404)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Service request creation error: {error_details}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def service_request_view(request, service_id=None):
    """Render the service request page"""
    service = None
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    else:
        # If no service_id provided, get the first available service
        service = Service.objects.first()
    
    if not service:
        from django.http import HttpResponse
        return HttpResponse("No services available. Please create a service first.", status=404)
    
    context = {
        'service': service
    }
    return render(request, 'service_request_new.html', context)
