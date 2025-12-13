# Service Request Quick Reference

## 🎯 Access the Page

```
http://127.0.0.1:8000/quotations/request/48/
```
Replace `48` with any service ID.

## 📊 Database Check

```bash
uv run python test_service_request_new.py
```

## 🧪 Test API

```bash
# Make sure server is running first
uv run python manage.py runserver

# In another terminal
uv run python test_api_submission.py
```

## 🔧 Admin Panel

```
http://127.0.0.1:8000/admin/quotations/servicerequest/
```

View all service requests with:
- Customer details
- Booking date & time
- Location coordinates
- Uploaded files
- Status tracking

## 📝 Form Steps

### Step 1: User Information
- First Name ✓
- Last Name ✓
- Email ✓
- Phone ✓

### Step 2: Booking Schedule
- **Calendar** (left column) - Select date
- **Time Slots** (right column) - Select time
- **Map** (full width) - Search and select location

### Step 3: Additional Items
- **File Upload** - Images, videos, PDFs (max 10MB each)
- **Notes** - Special requirements or instructions

### Step 4: Review
- Preview all information
- Submit request

## 🗂️ Data Saved

Every submission saves:
- User information → `quotations_servicerequest` table
- Files → `quotations_requestattachment` table + `media/quotations/`
- Location coordinates → lat/lng fields
- Booking details → date, time, datetime fields
- Status → 'pending' (default)

## 🔔 Auto Features

- ✅ WhatsApp notification sent automatically
- ✅ Total amount calculated (base + CC zone + VAT)
- ✅ Request ID generated
- ✅ Timestamp recorded

## 🎨 UI Components Used

From `/booking` page:
- ✓ Calendar widget
- ✓ Time slot picker  
- ✓ Map integration (OpenStreetMap + Leaflet)
- ✓ Location search

Custom additions:
- ✓ File upload with drag & drop
- ✓ Step wizard with progress
- ✓ Review screen
- ✓ Alpine.js state management

## 📱 Responsive Design

- Desktop: Full layout with sidebar
- Tablet: Stacked layout
- Mobile: Single column, optimized inputs

## 🛠️ Tech Stack

- **Frontend:** Alpine.js, Bootstrap 5, Leaflet.js
- **Backend:** Django, Python
- **Database:** SQLite (configurable)
- **File Storage:** Django media files
- **Map:** OpenStreetMap + Nominatim API

## 🚨 Validation

- Required fields enforced
- Date cannot be in past
- Time must be selected
- Location must be on map
- File types: jpg, png, mp4, pdf
- File size: max 10MB per file

## ✅ Success Flow

1. Form submitted → API called
2. Data validated → ServiceRequest created
3. Files saved → RequestAttachment records
4. WhatsApp sent → Notification delivered
5. User redirected → Home page
6. Admin notified → Can view in panel

## 🔗 Related Files

- Template: `templates/service_request_new.html`
- View: `quotations/views.py` → `create_service_request()`
- Model: `quotations/models.py` → `ServiceRequest`
- Admin: `quotations/admin.py` → `ServiceRequestAdmin`
- URL: `quotations/urls.py` → `/quotations/request/`

## 📈 Status Flow

```
pending → contacted → quoted → accepted → completed
         ↓
      rejected/cancelled
```

---

**Everything is working and ready to use!** 🎉
