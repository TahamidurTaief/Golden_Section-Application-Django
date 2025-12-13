import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from categories.models import Category
from services.models import Service
from providers.models import Provider

# Service data for each category (simplified)
services_data = {
    'Interior Design': [
        'Modern Home Interior Design',
        'Office Interior Design',
        'Kitchen Remodeling',
        'Bathroom Design & Renovation',
        'Living Room Makeover',
        'Bedroom Interior Design',
    ],
    'Construction': [
        'Residential Construction',
        'Commercial Building Construction',
        'Home Extension & Addition',
        'Structural Renovation',
        'Foundation Repair',
        'Roofing & Roof Replacement',
    ],
    'Plumbing Services': [
        'Emergency Plumbing Repair',
        'Water Heater Installation',
        'Bathroom Plumbing',
        'Kitchen Plumbing Installation',
        'Drain Cleaning & Unclogging',
        'Pipe Repair & Replacement',
    ],
    'Electrical Services': [
        'Electrical Panel Upgrade',
        'Home Rewiring',
        'Lighting Installation',
        'Electrical Outlet Installation',
        'Smart Home Electrical Setup',
        'Generator Installation',
    ],
    'Cleaning Services': [
        'Deep House Cleaning',
        'Office Cleaning Services',
        'Carpet & Upholstery Cleaning',
        'Window Cleaning',
        'Post-Construction Cleaning',
        'Move-In/Move-Out Cleaning',
    ],
    'Car Services': [
        'Full Car Detailing',
        'Engine Diagnostics & Repair',
        'Brake Service & Replacement',
        'Oil Change & Maintenance',
        'Tire Replacement & Alignment',
        'Car AC Repair & Service',
    ],
}

def add_services():
    # Get the first available provider
    provider = Provider.objects.first()
    
    if not provider:
        print("✗ No provider found in database. Please create a provider first.")
        return
    
    print(f"✓ Using provider: {provider.business_name}\n")
    
    total_added = 0
    
    for category_name, service_names in services_data.items():
        try:
            category = Category.objects.get(name=category_name)
            print(f"{'='*60}")
            print(f"Category: {category_name}")
            print(f"{'='*60}")
            
            for service_name in service_names:
                # Check if service already exists
                existing = Service.objects.filter(
                    name=service_name,
                    category=category
                ).first()
                
                if existing:
                    print(f"  ⊘ Skipped: {service_name} (already exists)")
                else:
                    service = Service.objects.create(
                        category=category,
                        provider=provider,
                        name=service_name,
                        slug=service_name.lower().replace('&', 'and').replace(' ', '-'),
                        short_description=f'Professional {service_name.lower()} services for your home or business.',
                        overview=f'Our expert team provides high-quality {service_name.lower()} with attention to detail and customer satisfaction.',
                        is_active=True,
                    )
                    print(f"  ✓ Added: {service_name}")
                    total_added += 1
            
            # Show final count for this category
            total_services = Service.objects.filter(category=category).count()
            print(f"  → Total services in {category_name}: {total_services}\n")
            
        except Category.DoesNotExist:
            print(f"✗ Category '{category_name}' not found. Skipping...\n")
    
    print(f"{'='*60}")
    print(f"✓ COMPLETE: Added {total_added} new services")
    print(f"{'='*60}\n")
    
    # Summary
    print("📊 FINAL SUMMARY:")
    print(f"{'='*60}")
    for category in Category.objects.all():
        service_count = Service.objects.filter(category=category).count()
        status = "✓" if service_count >= 6 else "⚠"
        print(f"{status} {category.name}: {service_count} services")

if __name__ == '__main__':
    add_services()
