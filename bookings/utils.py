import urllib.parse
from datetime import datetime
from django.utils import timezone


def send_whatsapp_notification(booking):
    """
    Send WhatsApp notification for a booking.
    Returns True if successful, False otherwise.
    
    Note: This generates a WhatsApp Web URL that can be opened to send the message.
    For automated sending, you would need to integrate with WhatsApp Business API.
    """
    try:
        # Get WhatsApp number
        whatsapp_number = booking.get_whatsapp_number()
        
        if not whatsapp_number:
            print(f"No WhatsApp number available for booking {booking.booking_reference}")
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
        message = build_booking_message(booking)
        
        # Update booking record
        booking.whatsapp_number_used = whatsapp_number
        booking.whatsapp_sent = True
        booking.whatsapp_sent_at = timezone.now()
        booking.save(update_fields=['whatsapp_number_used', 'whatsapp_sent', 'whatsapp_sent_at'])
        
        # Generate WhatsApp URL (for manual or automated sending)
        whatsapp_url = generate_whatsapp_url(whatsapp_number, message)
        
        print(f"WhatsApp notification prepared for booking {booking.booking_reference}")
        print(f"WhatsApp URL: {whatsapp_url}")
        
        return True
        
    except Exception as e:
        import traceback
        print(f"Error sending WhatsApp notification for booking {booking.booking_reference}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False


def build_booking_message(booking):
    """Build WhatsApp message content for booking"""
    from datetime import datetime
    
    # Sub-services list
    sub_services_text = ""
    if booking.sub_services.exists():
        sub_services_list = "\n".join([f"  • {sub.name}" for sub in booking.sub_services.all()])
        sub_services_text = f"\n\n*Services Requested:*\n{sub_services_list}"
    
    # Provider info
    provider_text = ""
    if booking.provider:
        provider_text = f"\n*Provider:* {booking.provider.business_name}"
    
    # Format appointment date safely
    if isinstance(booking.appointment_date, str):
        # If it's a string, parse it
        try:
            date_obj = datetime.strptime(booking.appointment_date, '%Y-%m-%d').date()
            formatted_date = date_obj.strftime('%A, %B %d, %Y')
        except:
            formatted_date = booking.appointment_date
    else:
        # If it's already a date object
        formatted_date = booking.appointment_date.strftime('%A, %B %d, %Y')
    
    # Build message
    message = f"""
🔔 *New Appointment Booking*

*Booking Reference:* {booking.booking_reference}
*Status:* {booking.get_status_display()}

*Customer Information:*
👤 Name: {booking.customer_full_name}
📧 Email: {booking.customer_email}
📱 Phone: {booking.customer_phone}

*Service Details:*
🔧 Service: {booking.service.name}
📂 Category: {booking.service.category.name}{provider_text}{sub_services_text}

*Appointment:*
📅 Date: {formatted_date}
⏰ Time: {booking.appointment_time}

*Service Location:*
📍 {booking.location_address}
🗺️ Map: {booking.google_maps_link}
""".strip()
    
    if booking.notes:
        message += f"\n\n💬 *Customer Notes:*\n{booking.notes}"
    
    message += f"\n\n⏱️ _Booked on {booking.created_at.strftime('%B %d, %Y at %I:%M %p')}_"
    
    return message


def generate_whatsapp_url(phone_number, message):
    """Generate WhatsApp Web URL"""
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone_number}?text={encoded_message}"


def get_whatsapp_web_url(booking):
    """Get WhatsApp Web URL for a booking (for frontend use)"""
    try:
        whatsapp_number = booking.get_whatsapp_number()
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
        
        message = build_booking_message(booking)
        return generate_whatsapp_url(whatsapp_number, message)
    except Exception as e:
        import traceback
        print(f"Error generating WhatsApp URL for booking {booking.booking_reference}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None
