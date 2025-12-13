# Quick Start - Testing Booking System

## 1. Ensure Migrations Are Applied
```bash
uv run manage.py migrate
```

## 2. Create/Update Site Configuration
```bash
uv run manage.py shell
```

```python
from site_config.models import SiteConfiguration

config = SiteConfiguration.load()
config.default_whatsapp = '+971501234567'  # Your WhatsApp number
config.save()
exit()
```

## 3. Start Development Server
```bash
uv run manage.py runserver
```

## 4. Test Booking Flow

### Step 1: Go to a Service
1. Visit: `http://127.0.0.1:8000/`
2. Click on any service
3. Click "Book Now" button

### Step 2: Fill Booking Form
1. **Customer Information**:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Phone: +971501234567

2. **Select Services**: Check at least one sub-service

3. **Select Location**: 
   - Either search for a location in Dubai
   - Or click on the map
   - Address will auto-fill

4. **Select Date**: Pick a future date from calendar

5. **Select Time**: Choose a time slot

6. **Click "Book Appointment"**

### Step 3: Verify Success
- You should see a success message
- Option to send via WhatsApp
- Redirect to home after 2 seconds

## 5. Check Admin Panel

### Access Admin:
```bash
# If you don't have a superuser:
uv run manage.py createsuperuser
```

1. Visit: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Click "Bookings" → "Bookings"
4. You should see your test booking

### Admin Features to Test:
- View booking details
- Change status to "Confirmed"
- Click "Resend WhatsApp Notification"
- Click Google Maps link
- Filter by status, date
- Search by customer name

## 6. Test WhatsApp URL

When booking is created, you'll get a WhatsApp URL like:
```
https://wa.me/971501234567?text=...
```

Click this to open WhatsApp Web with the pre-filled message.

## Common Test Scenarios

### Test 1: Complete Booking
- Fill all fields correctly
- Should create booking successfully
- Should get booking reference

### Test 2: Validation
- Try submitting without filling all fields
- Should show validation errors

### Test 3: Multiple Sub-services
- Select 3+ sub-services
- Should save all selections
- Should display in success page

### Test 4: Location Selection
- Search for "Dubai Marina"
- Click on a result
- Map should update
- Address should be set

### Test 5: Admin Status Change
- Create booking (status: Pending)
- In admin, change to "Confirmed"
- Verify it updates

## Troubleshooting

### "CSRF token missing"
Add to your booking.html (already done):
```html
{% csrf_token %}
```

### "Service not found"
Ensure you're accessing booking page from a valid service:
```
http://127.0.0.1:8000/booking/1/
```
Replace `1` with actual service ID.

### WhatsApp number not working
Check format in Site Configuration:
- ✅ Good: `+971501234567`
- ❌ Bad: `0501234567` (missing country code)
- ❌ Bad: `+971 50 123 4567` (has spaces)

### Map not loading
Check browser console for errors. Ensure:
- Leaflet library is loaded
- Internet connection is active

## Sample Booking Data

For quick testing, use this data:

```json
{
  "customer_first_name": "John",
  "customer_last_name": "Doe",
  "customer_email": "john.doe@example.com",
  "customer_phone": "+971501234567",
  "location_address": "Dubai Marina, Dubai, UAE",
  "location_lat": "25.0772",
  "location_lng": "55.1364",
  "appointment_date": "2024-12-20",
  "appointment_time": "10:00 AM"
}
```

## Expected Results

### Database Record:
- New entry in `bookings` table
- Booking reference: `BK-20241211-XXXX`
- Status: `pending`
- WhatsApp sent: `True`

### Admin Display:
- Booking visible in list
- Status badge shows "Pending" (orange)
- WhatsApp status shows "✓ Sent" (green)

### Success Page Shows:
- ✅ Booking reference
- ✅ Customer details
- ✅ Service name
- ✅ Selected sub-services
- ✅ Date and time
- ✅ Location with Google Maps link
- ✅ WhatsApp send button

## Next Steps After Testing

1. **Add real phone numbers** in Site Configuration
2. **Test actual WhatsApp sending** (open the URL on phone)
3. **Customize email notifications** (future feature)
4. **Add booking confirmation emails** (requires SMTP)
5. **Enable customer accounts** for booking history

---

**Ready to Test!** 🚀

Follow the steps above and everything should work smoothly.
