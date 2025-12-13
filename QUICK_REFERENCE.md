# Quick Start Guide - Service Request System

## 🚀 Quick Commands

```bash
# Navigate to project
cd C:\Users\iZoom10\Desktop\Golden_Section

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run migrations (if needed)
python manage.py migrate

# Start server
python manage.py runserver

# Test the system
python test_service_request.py
```

## 📋 Current Form Fields

### Required Fields:
- First Name
- Last Name  
- Email Address
- Phone Number
- Booking Estimate (0-2, 2-3, 3-4, 4+ hours)
- Booking Date & Time
- Hourly Rate (£70 or £90)

### Optional Fields:
- CC Zone checkbox
- Number of People
- File attachments (images/videos)
- Additional notes

## 🔗 Important URLs

```
Service Request Form: /quotations/request/
Service Request with ID: /quotations/request/<service_id>/
Admin Panel: /admin/quotations/servicerequest/
```

## 💾 Database Schema

```python
ServiceRequest Model:
- service (ForeignKey to Service)
- first_name, last_name, email, phone
- pricing_tier, booking_estimate, booking_datetime
- number_of_people, hourly_rate
- additional_notes, cc_zone
- booking_charges, cc_zone_charge, vat, total_amount
- status, whatsapp_sent, whatsapp_sent_at
- created_at, updated_at
```

## 🧪 Test Data

```python
# Create test service request
from quotations.models import ServiceRequest
from services.models import Service
from datetime import datetime, timedelta

service = Service.objects.first()
ServiceRequest.objects.create(
    service=service,
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    phone='+971501234567',
    booking_estimate='2-3',
    booking_datetime=datetime.now() + timedelta(days=1),
    number_of_people=2,
    hourly_rate=70.00,
    cc_zone=False
)
```

## ✅ Verification

```bash
# Check if data saves correctly
python manage.py shell -c "from quotations.models import ServiceRequest; print(f'Total: {ServiceRequest.objects.count()}')"

# View latest request
python manage.py shell -c "from quotations.models import ServiceRequest; sr = ServiceRequest.objects.last(); print(f'ID: {sr.id}, Customer: {sr.customer_name}, Total: £{sr.total_amount}')"
```

## 🐛 Troubleshooting

### Issue: Form doesn't submit
1. Check browser console (F12)
2. Verify CSRF token is present
3. Check network tab for API errors

### Issue: Data not saving
1. Check terminal for Python errors
2. Verify migrations are applied: `python manage.py migrate`
3. Run test script: `python test_service_request.py`

### Issue: WhatsApp not sending
1. Check service/category has WhatsApp number configured
2. Check site configuration has default WhatsApp
3. Verify phone number format is correct

## 📊 Cost Calculation Formula

```
Base = £42.00
CC_Zone = £15.00 (if checked, else £0.00)
Hourly = £70.00 or £90.00 (user selected)

Subtotal = Base + CC_Zone + Hourly
VAT = Subtotal × 0.20
Total = Subtotal + VAT
```

## 🎯 Next Steps

1. Test form in browser: http://127.0.0.1:8000/quotations/request/
2. Submit a test request
3. Verify data in admin panel
4. Check WhatsApp message generation
5. Deploy to production

---

**Status**: ✅ All systems operational
**Last Verified**: December 11, 2025
