# Booking System Documentation

## Overview
Complete appointment booking system with WhatsApp integration for the Golden Section service marketplace.

## Features Implemented

### 1. **UI Improvements**
- ✅ Reduced Appointment Time section height from 360px to 250px for better layout
- ✅ Fixed button positioning - Book Appointment button now displays properly after sections
- ✅ Improved responsive design for mobile devices

### 2. **Database Model** (`bookings/models.py`)
The `Booking` model includes:

#### Core Fields:
- **Service Information**: Service, Provider, Sub-services (M2M)
- **Customer Details**: First name, Last name, Email, Phone
- **Location Data**: Latitude, Longitude, Full address
- **Appointment**: Date, Time (string format like "10:00 AM")
- **Status**: Pending, Confirmed, In Progress, Completed, Cancelled

#### Unique Features:
- **Auto-generated booking reference**: Format `BK-YYYYMMDD-XXXX` (e.g., `BK-20251211-A1B2`)
- **WhatsApp tracking**: Sent status, timestamp, number used
- **Google Maps integration**: Auto-generates map links from coordinates

#### Removed Fields:
- ❌ Collection address (as requested)
- ❌ Delivery address (as requested)

### 3. **WhatsApp Integration** (`bookings/utils.py`)

#### `send_whatsapp_notification(booking)`
Automatically sends WhatsApp notification when booking is created.

**WhatsApp Number Priority** (in order):
1. Service-specific WhatsApp (`service.whatsapp_number`)
2. Category WhatsApp (`category.whatsapp_number`)
3. Default WhatsApp from Site Configuration (`site_config.default_whatsapp`)

**Message Format**:
```
🔔 *New Appointment Booking*

*Booking Reference:* BK-20251211-A1B2
*Status:* Pending

*Customer Information:*
👤 Name: John Doe
📧 Email: john@example.com
📱 Phone: +971501234567

*Service Details:*
🔧 Service: Electrical Maintenance
📂 Category: Home Services
*Provider:* ABC Services

*Services Requested:*
  • Fan Repair
  • AC Installation

*Appointment:*
📅 Date: Wednesday, December 11, 2024
🕐 Time: 10:00 AM

*Service Location:*
📍 123 Main St, Dubai Marina, Dubai, UAE
🗺️ Map: https://www.google.com/maps?q=25.0772,55.1364

_Booked on December 11, 2024 at 10:30 AM_
```

### 4. **API Endpoints**

#### `POST /bookings/create/`
Creates a new booking.

**Request Body (JSON)**:
```json
{
  "service_id": 1,
  "provider_id": 1,
  "customer_first_name": "John",
  "customer_last_name": "Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+971501234567",
  "location_lat": 25.0772,
  "location_lng": 55.1364,
  "location_address": "123 Main St, Dubai Marina, Dubai",
  "appointment_date": "2024-12-15",
  "appointment_time": "10:00 AM",
  "selected_sub_services": [1, 2, 3],
  "notes": "Please call before arriving"
}
```

**Response**:
```json
{
  "success": true,
  "booking_reference": "BK-20251211-A1B2",
  "message": "Booking created successfully!",
  "whatsapp_sent": true,
  "whatsapp_url": "https://wa.me/971501234567?text=...",
  "booking_details": {
    "reference": "BK-20251211-A1B2",
    "customer_name": "John Doe",
    "service_name": "Electrical Maintenance",
    "appointment": "December 15, 2024 at 10:00 AM",
    "status": "Pending"
  }
}
```

#### `GET /bookings/success/<booking_reference>/`
Displays booking confirmation page.

#### `GET /bookings/my-bookings/`
Lists all customer bookings (requires authentication - future enhancement).

### 5. **Admin Panel** (`bookings/admin.py`)

#### Features:
- **List Display**: Reference, Customer, Service, Appointment, Status, WhatsApp Status
- **Filters**: Status, WhatsApp sent, Date, Category
- **Search**: Reference, Customer name, Email, Phone
- **Colored Status Badges**: Visual status indicators
- **Google Maps Links**: Direct links to service locations

#### Bulk Actions:
- Mark as Confirmed
- Mark as Completed
- Mark as Cancelled
- Resend WhatsApp Notification

#### Field Organization:
- Booking Information
- Customer Information
- Appointment Details
- Location (with Google Maps link)
- Notes (collapsible)
- WhatsApp Notification (collapsible)
- Metadata (collapsible)

### 6. **Frontend Integration** (`templates/booking.html`)

#### JavaScript Function: `submitBooking()`
- ✅ Complete validation of all fields
- ✅ AJAX submission to `/bookings/create/`
- ✅ Success message with booking reference
- ✅ Optional WhatsApp redirect popup
- ✅ Auto-redirect to home page after 2 seconds

#### Form Validation:
- Customer first & last name required
- Email & phone required
- At least one sub-service must be selected
- Location must be selected on map
- Date and time must be selected

### 7. **Success Page** (`templates/booking_success.html`)
Beautiful confirmation page showing:
- ✅ Success icon and message
- ✅ Booking reference (large, prominent)
- ✅ All booking details organized in sections
- ✅ Selected sub-services as badges
- ✅ Google Maps link
- ✅ WhatsApp send button
- ✅ Back to home button

## Installation & Setup

### 1. Add to `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'bookings',
]
```

### 2. Include URLs in `urls.py`:
```python
urlpatterns = [
    # ... other patterns
    path('bookings/', include('bookings.urls')),
]
```

### 3. Run Migrations:
```bash
python manage.py makemigrations bookings
python manage.py migrate
```

### 4. Configure Default WhatsApp:
Go to Admin → Site Configuration and set `default_whatsapp` field.

Format: `+971501234567` (with country code)

## Usage Flow

### Customer Journey:
1. **Browse Services** → Service Details Page
2. **Click "Book Now"** → Booking Page
3. **Fill Customer Info** (Name, Email, Phone)
4. **Select Sub-services** (one or more)
5. **Choose Location** on map
6. **Select Date & Time**
7. **Click "Book Appointment"**
8. **See Success Page** with booking reference
9. **Optional**: Send details via WhatsApp

### Backend Processing:
1. Validate all inputs
2. Create booking in database
3. Generate unique reference number
4. Associate selected sub-services
5. Send WhatsApp notification
6. Return success response with WhatsApp URL
7. Update booking status

### Admin Management:
1. View all bookings in admin panel
2. Filter by status, date, category
3. Update booking status
4. Add admin notes
5. Resend WhatsApp notifications
6. View customer details and location

## WhatsApp Integration Details

### Number Selection Logic:
```python
def get_whatsapp_number():
    if service.whatsapp_number:
        return service.whatsapp_number
    elif service.category.whatsapp_number:
        return service.category.whatsapp_number
    else:
        return site_config.default_whatsapp
```

### Number Formatting:
- Removes spaces, dashes, special characters
- Converts `0501234567` → `971501234567` (UAE)
- Ensures proper country code

### Message Generation:
- Professional formatting with emojis
- All booking details included
- Google Maps link for location
- Customer notes if provided
- Timestamp of booking

## Model Properties & Methods

### `Booking` Model:

**Properties**:
- `customer_full_name` → Combined first + last name
- `formatted_appointment_datetime` → Human-readable date/time
- `sub_services_list` → Comma-separated sub-service names
- `google_maps_link` → Google Maps URL from coordinates

**Methods**:
- `save()` → Auto-generates booking reference
- `get_whatsapp_number()` → Returns appropriate WhatsApp number

## Future Enhancements

### Potential Features:
- [ ] Email notifications (SMTP integration)
- [ ] SMS notifications (Twilio integration)
- [ ] User authentication & customer accounts
- [ ] Booking calendar view
- [ ] Provider dashboard
- [ ] Payment integration
- [ ] Booking reminders (24h before)
- [ ] Rating & review system after completion
- [ ] Booking modification/cancellation by customer
- [ ] Real-time WhatsApp API (WhatsApp Business API)

## Database Schema

```
Booking
├── id (PK)
├── booking_reference (Unique)
├── service (FK → Service)
├── provider (FK → Provider)
├── sub_services (M2M → SubService)
├── customer_first_name
├── customer_last_name
├── customer_email
├── customer_phone
├── location_latitude
├── location_longitude
├── location_address
├── appointment_date
├── appointment_time
├── status (pending/confirmed/in_progress/completed/cancelled)
├── notes
├── admin_notes
├── whatsapp_sent
├── whatsapp_sent_at
├── whatsapp_number_used
├── created_at
└── updated_at
```

## Testing Checklist

- [x] Create booking with valid data
- [x] Validate required fields
- [x] Save booking to database
- [x] Generate unique booking reference
- [x] Associate sub-services
- [x] WhatsApp notification generation
- [x] Display success page
- [x] Admin panel displays bookings
- [x] Status update works
- [x] Google Maps links work
- [ ] Test with actual WhatsApp (requires phone)
- [ ] Email notification (requires SMTP)

## Troubleshooting

### WhatsApp not sending?
1. Check `default_whatsapp` in Site Configuration
2. Verify number format: `+971501234567`
3. Check service/category has WhatsApp number set
4. Review `whatsapp_sent` flag in booking

### Booking not saving?
1. Check all required fields are filled
2. Verify service_id exists
3. Check validation errors in browser console
4. Review Django error logs

### Admin panel errors?
1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Check `bookings` app in INSTALLED_APPS

## Files Modified/Created

### Created:
- `bookings/` - New Django app
- `bookings/models.py` - Booking model
- `bookings/views.py` - Booking views
- `bookings/admin.py` - Admin configuration
- `bookings/utils.py` - WhatsApp utilities
- `bookings/urls.py` - URL patterns
- `bookings/migrations/0001_initial.py` - Initial migration
- `templates/booking_success.html` - Success page

### Modified:
- `templates/booking.html` - Added submitBooking() function
- `GoldenSection/settings.py` - Added 'bookings' to INSTALLED_APPS
- `GoldenSection/urls.py` - Added bookings URLs

## Support

For issues or questions:
1. Check Django error logs
2. Review browser console for JavaScript errors
3. Verify database migrations are applied
4. Ensure all dependencies are installed

---

**Version**: 1.0.0  
**Date**: December 11, 2024  
**Author**: Golden Section Development Team
