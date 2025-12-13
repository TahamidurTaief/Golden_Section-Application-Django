from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import json

from services.models import Service, SubService
from providers.models import Provider
from .models import Booking
from .utils import send_whatsapp_notification, get_whatsapp_web_url


@require_http_methods(["POST"])
@csrf_exempt
def create_booking(request):
    """Create a new booking from the booking form"""
    try:
        # Parse JSON data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Validate required fields
        required_fields = [
            'service_id', 'customer_first_name', 'customer_last_name',
            'customer_email', 'customer_phone', 'location_lat', 'location_lng',
            'location_address', 'appointment_date', 'appointment_time'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
        
        # Get service
        service = get_object_or_404(Service, id=data['service_id'])
        
        # Get provider if available
        provider = None
        if data.get('provider_id'):
            provider = Provider.objects.filter(id=data['provider_id']).first()
        
        # Parse appointment date - convert string to date object
        appointment_date_str = data['appointment_date']
        if isinstance(appointment_date_str, str):
            # Try multiple date formats
            for date_format in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                try:
                    appointment_date = datetime.strptime(appointment_date_str, date_format).date()
                    break
                except ValueError:
                    continue
            else:
                # If no format matches, raise error
                raise ValueError(f"Invalid date format: {appointment_date_str}. Expected format: YYYY-MM-DD")
        else:
            appointment_date = appointment_date_str
        
        # Validate and format appointment time
        appointment_time = str(data['appointment_time']).strip()
        
        # Parse and validate location coordinates
        try:
            location_latitude = float(data['location_lat'])
            location_longitude = float(data['location_lng'])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid location coordinates: {str(e)}")
        
        # Create booking - STEP 1: Save to Database
        print(f"Creating booking with data: service_id={service.id}, customer={data['customer_first_name']} {data['customer_last_name']}")
        
        booking = Booking.objects.create(
            service=service,
            provider=provider,
            customer_first_name=data['customer_first_name'].strip(),
            customer_last_name=data['customer_last_name'].strip(),
            customer_email=data['customer_email'].strip().lower(),
            customer_phone=data['customer_phone'].strip(),
            location_latitude=location_latitude,
            location_longitude=location_longitude,
            location_address=data['location_address'].strip(),
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            notes=data.get('notes', '').strip()
        )
        
        print(f"✅ STEP 1: Booking saved to database with ID={booking.id}, Reference={booking.booking_reference}")
        
        # Add sub-services if selected
        selected_sub_services = data.get('selected_sub_services', [])
        if isinstance(selected_sub_services, str):
            try:
                selected_sub_services = json.loads(selected_sub_services)
            except:
                selected_sub_services = []
        
        if selected_sub_services:
            # Extract IDs from sub-services array
            sub_service_ids = []
            for item in selected_sub_services:
                if isinstance(item, dict) and 'id' in item:
                    sub_service_ids.append(item['id'])
                elif isinstance(item, (int, str)):
                    sub_service_ids.append(item)
            
            if sub_service_ids:
                sub_services = SubService.objects.filter(
                    id__in=sub_service_ids,
                    service=service
                )
                booking.sub_services.set(sub_services)
                print(f"✅ Added {sub_services.count()} sub-services to booking")
        
        # STEP 2: Send WhatsApp notification
        print(f"🔄 STEP 2: Sending WhatsApp notification for booking {booking.booking_reference}")
        try:
            whatsapp_sent = send_whatsapp_notification(booking)
            if whatsapp_sent:
                print(f"✅ STEP 2: WhatsApp notification sent successfully")
            else:
                print(f"⚠️ STEP 2: WhatsApp notification failed but booking is saved")
        except Exception as e:
            print(f"❌ WhatsApp notification error for booking {booking.booking_reference}: {str(e)}")
            import traceback
            print(traceback.format_exc())
            whatsapp_sent = False
        
        # Generate WhatsApp URL for redirect
        try:
            whatsapp_url = get_whatsapp_web_url(booking)
        except Exception as e:
            print(f"WhatsApp URL generation failed for booking {booking.booking_reference}: {str(e)}")
            whatsapp_url = None
        
        return JsonResponse({
            'success': True,
            'booking_reference': booking.booking_reference,
            'message': 'Booking created successfully!',
            'whatsapp_sent': whatsapp_sent,
            'whatsapp_url': whatsapp_url,
            'booking_details': {
                'reference': booking.booking_reference,
                'customer_name': booking.customer_full_name,
                'service_name': booking.service.name,
                'appointment': booking.formatted_appointment_datetime,
                'status': booking.get_status_display()
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
        print(f"Booking creation error: {error_details}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def booking_success(request, booking_reference):
    """Booking success page"""
    booking = get_object_or_404(Booking, booking_reference=booking_reference)
    whatsapp_url = get_whatsapp_web_url(booking)
    
    context = {
        'booking': booking,
        'whatsapp_url': whatsapp_url
    }
    return render(request, 'booking_success.html', context)


def my_bookings(request):
    """List customer bookings (requires authentication in future)"""
    # For now, show all bookings (in production, filter by user)
    bookings = Booking.objects.all().select_related(
        'service',
        'provider',
        'service__category'
    ).prefetch_related('sub_services')
    
    context = {
        'bookings': bookings
    }
    return render(request, 'my_bookings.html', context)
