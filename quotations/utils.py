import urllib.parse
from datetime import datetime
from django.utils import timezone


def send_whatsapp_quotation(service_request):
    """
    Send WhatsApp notification for a service request.
    Returns True if successful, False otherwise.
    """
    try:
        # Get WhatsApp number
        whatsapp_number = service_request.get_whatsapp_number()
        
        if not whatsapp_number:
            print(f"No WhatsApp number available for service request {service_request.id}")
            return False
        
        # Get country code from site configuration
        try:
            from site_config.models import SiteConfiguration
            config = SiteConfiguration.load()
            country_code = config.default_country_code if config and config.default_country_code else '971'
        except Exception:
            country_code = '971'
        
        # Clean WhatsApp number (remove spaces, dashes, etc.)
        whatsapp_number = ''.join(filter(str.isdigit, whatsapp_number))
        if whatsapp_number.startswith('0'):
            whatsapp_number = country_code + whatsapp_number[1:]
        elif not whatsapp_number.startswith('+'):
            if not whatsapp_number.startswith(country_code):
                whatsapp_number = country_code + whatsapp_number
        
        # Build message
        message = build_quotation_message(service_request)
        
        # Update service request record
        service_request.whatsapp_number_used = whatsapp_number
        service_request.whatsapp_sent = True
        service_request.whatsapp_sent_at = timezone.now()
        service_request.save(update_fields=['whatsapp_number_used', 'whatsapp_sent', 'whatsapp_sent_at'])
        
        # Generate WhatsApp URL
        whatsapp_url = generate_whatsapp_url(whatsapp_number, message)
        
        print(f"WhatsApp notification prepared for service request {service_request.id}")
        print(f"WhatsApp URL: {whatsapp_url}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"Error sending WhatsApp notification for service request {service_request.id}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False


def build_quotation_message(service_request):
    """Build WhatsApp message content for service request quotation"""
    
    # Format booking datetime
    if isinstance(service_request.booking_datetime, str):
        try:
            datetime_obj = datetime.strptime(service_request.booking_datetime, '%Y-%m-%d %H:%M:%S')
            formatted_datetime = datetime_obj.strftime('%A, %B %d, %Y at %I:%M %p')
        except (ValueError, AttributeError):
            formatted_datetime = service_request.booking_datetime
    else:
        formatted_datetime = service_request.booking_datetime.strftime('%A, %B %d, %Y at %I:%M %p')
    
    # Build message
    message = f"""
🚚 *NEW SERVICE REQUEST*

*Request ID:* {service_request.id}
*Status:* {service_request.get_status_display()}

*Customer Information:*
👤 Name: {service_request.customer_name}
📧 Email: {service_request.email}
📱 Phone: {service_request.phone}

*Service Details:*
🔧 Service: {service_request.service.name}
📂 Category: {service_request.service.category.name}

*Booking Schedule:*
📅 Date & Time: {formatted_datetime}
""".strip()
    
    # Add location if available
    if service_request.location_address:
        message += f"""

*Location:*
📍 {service_request.location_address}
"""
        
        # Add map link if coordinates are available
        if service_request.location_latitude and service_request.location_longitude:
            message += f"🗺️ Map: https://www.google.com/maps?q={service_request.location_latitude},{service_request.location_longitude}"
    
    # Add additional notes if provided
    if service_request.additional_notes:
        message += f"""

💬 *Additional Notes:*
{service_request.additional_notes}
"""
    
    message += f"""

⏱️ _Submitted on {service_request.created_at.strftime('%B %d, %Y at %I:%M %p')}_
"""
    
    return message


def generate_whatsapp_url(phone_number, message):
    """Generate WhatsApp Web URL"""
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone_number}?text={encoded_message}"


def get_whatsapp_quotation_url(service_request):
    """Get WhatsApp Web URL for a service request (for frontend use)"""
    try:
        whatsapp_number = service_request.get_whatsapp_number()
        if not whatsapp_number:
            return None
        
        # Get country code from site configuration
        try:
            from site_config.models import SiteConfiguration
            config = SiteConfiguration.load()
            country_code = config.default_country_code if config and config.default_country_code else '971'
        except Exception:
            country_code = '971'
        
        # Clean number
        whatsapp_number = ''.join(filter(str.isdigit, whatsapp_number))
        if not whatsapp_number:
            return None
            
        if whatsapp_number.startswith('0'):
            whatsapp_number = country_code + whatsapp_number[1:]
        elif not whatsapp_number.startswith(country_code):
            whatsapp_number = country_code + whatsapp_number
        
        message = build_quotation_message(service_request)
        return generate_whatsapp_url(whatsapp_number, message)
    except Exception as e:
        import traceback
        print(f"Error generating WhatsApp URL for service request {service_request.id}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None
