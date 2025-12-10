# Quick Start Guide - Golden Section Backend

## 🚀 Server is Ready!

### Admin Access
- **URL:** http://localhost:8000/admin/
- **Username:** `admin`
- **Password:** `admin123`

---

## 📦 What's Been Created

### Apps & Models
✅ **7 Django apps** with **24 models**
✅ **Custom User model** with role-based access
✅ **All admin panels** configured and working
✅ **Database migrations** applied
✅ **Superuser account** created

### Key Apps:
1. **accounts** - User management (customers, providers, admins)
2. **site_config** - Site-wide settings (logo, WhatsApp, meta tags, etc.)
3. **categories** - Service categories & subcategories
4. **services** - Services with 3-tier pricing (Basic, Standard, Premium)
5. **providers** - Provider profiles, gallery, reviews
6. **quotations** - Service request & quotation system
7. **content** - Pages, FAQ, Blog, Testimonials, Contact

---

## 🎯 Core Features Implemented

### 1. Site Configuration
- Single admin panel for all site settings
- Default WhatsApp number
- Google Analytics & Facebook Pixel IDs
- Footer content & important links
- Available globally in templates: `{{ site_config.site_name }}`

### 2. WhatsApp System (3-Level Hierarchy)
```
Priority:
1. Service-specific WhatsApp
2. Category WhatsApp
3. Default site WhatsApp
```
Every service can have its own WhatsApp number!

### 3. Quotation System
Complete service request form with:
- Customer information
- Service selection (with pricing tier)
- Collection & delivery addresses
- Property details (type, bedrooms, floor, lift)
- Automatic price calculation (charges + CC zone + VAT)
- File attachments
- Admin quotation responses
- WhatsApp integration ready

### 4. Three-Tier Pricing
Every service can have:
- **Basic** package
- **Standard** package  
- **Premium** package

Each with:
- Custom price
- Description
- Feature list (JSON)
- "Recommended" flag

---

## 🔧 Admin Features

### Advanced Filtering
- Filter by categories, status, dates
- Search across multiple fields
- Bulk actions

### Inline Management
- Add subcategories from category page
- Add pricing tiers from service page
- Add gallery images inline
- Add quotations from request page

### Smart Fields
- Auto-slug generation
- Auto-calculation (quotation totals)
- View counters
- Rating calculations

---

## 📊 Database Schema

### User System
```
User (Custom)
  ├── role (customer/provider/admin)
  ├── profile info
  └── verification status
```

### Service Flow
```
Category
  └── SubCategory
      └── Service
          ├── PricingTiers (Basic, Standard, Premium)
          └── Gallery
```

### Provider System
```
Provider
  ├── Business info
  ├── Services (ManyToMany)
  ├── Gallery
  └── Reviews
```

### Quotation Flow
```
ServiceRequest
  ├── Customer info
  ├── Service + Tier
  ├── Addresses
  ├── Attachments
  └── QuotationResponse
```

---

## 🎨 Next Development Steps

### Phase 1: Frontend Views
1. Home page with featured services
2. Category listing & detail pages
3. Service listing & detail pages
4. Service request form
5. Provider listing & detail pages

### Phase 2: Authentication
1. Login/Register forms
2. Password reset
3. User dashboard
4. Provider dashboard

### Phase 3: Integrations
1. WhatsApp API for auto-messaging
2. Email notifications
3. Payment gateway (optional)

### Phase 4: Enhancement
1. Search & filtering
2. AJAX form submissions
3. Image optimization
4. SEO optimization
5. Performance tuning

---

## 💻 Useful Commands

### Run Development Server
```bash
uv run manage.py runserver
```

### Create Migrations (after model changes)
```bash
uv run manage.py makemigrations
uv run manage.py migrate
```

### Access Django Shell
```bash
uv run manage.py shell
```

### Create Another Admin User
```bash
uv run manage.py createsuperuser
```

---

## 📝 Model Examples

### Adding a Category via Shell
```python
from categories.models import Category

category = Category.objects.create(
    name="Home Cleaning",
    description="Professional home cleaning services",
    whatsapp_number="+447123456789",
    is_featured=True
)
```

### Adding a Service
```python
from services.models import Service, ServicePricingTier

service = Service.objects.create(
    category=category,
    name="Deep House Cleaning",
    short_description="Complete house cleaning service",
    description="Full description here...",
    whatsapp_number="+447987654321",
    is_featured=True
)

# Add pricing tiers
ServicePricingTier.objects.create(
    service=service,
    tier_type='basic',
    name='Basic Clean',
    price=50.00,
    description='Standard cleaning',
    features=['Kitchen', 'Bathroom', 'Living room']
)
```

### Adding Site Configuration
```python
from site_config.models import SiteConfiguration

config = SiteConfiguration.load()
config.site_name = "Golden Section"
config.primary_email = "info@goldensection.com"
config.default_whatsapp = "+447000000000"
config.google_analytics_id = "G-XXXXXXXXXX"
config.facebook_pixel_id = "123456789"
config.save()
```

---

## 🔍 Testing Admin Panels

Visit these admin sections:
- http://localhost:8000/admin/accounts/user/
- http://localhost:8000/admin/site_config/siteconfiguration/
- http://localhost:8000/admin/categories/category/
- http://localhost:8000/admin/services/service/
- http://localhost:8000/admin/providers/provider/
- http://localhost:8000/admin/quotations/servicerequest/
- http://localhost:8000/admin/content/page/

---

## 🎯 Template Usage

### Access Site Config Anywhere
```django
{{ site_config.site_name }}
{{ site_config.logo.url }}
{{ site_config.default_whatsapp }}
{{ site_config.google_analytics_id }}
```

### Get Service WhatsApp
```python
service.get_whatsapp()  # Returns service > category > default
```

---

## 📚 Documentation

See `BACKEND_STRUCTURE.md` for:
- Complete model documentation
- All relationships
- Admin features
- Design patterns used

---

## ✅ System Check Passed

All Django checks passed successfully!
Ready for development! 🚀

---

**Created:** December 10, 2025
**Status:** ✅ Production-Ready Backend Structure
