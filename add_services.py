import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoldenSection.settings')
django.setup()

from categories.models import Category
from services.models import Service
from providers.models import Provider
from decimal import Decimal

# Service data for each category
services_data = {
    'Interior Design': [
        {
            'name': 'Modern Home Interior Design',
            'short_description': 'Contemporary interior design for residential spaces with minimalist aesthetics and functional layouts.',
        },
        {
            'name': 'Office Interior Design',
            'short_description': 'Professional workspace design that enhances productivity and creates inspiring work environments.',
        },
        {
            'name': 'Kitchen Remodeling',
            'short_description': 'Complete kitchen renovation with custom cabinetry, modern appliances, and efficient layouts.',
        },
        {
            'name': 'Bathroom Design & Renovation',
            'short_description': 'Luxury bathroom design with premium fixtures, elegant tiles, and spa-like ambiance.',
        },
        {
            'name': 'Living Room Makeover',
            'short_description': 'Transform your living space with stylish furniture, color schemes, and lighting design.',
        },
        {
            'name': 'Bedroom Interior Design',
            'short_description': 'Create peaceful and comfortable bedroom spaces with custom furniture and décor.',
        },
    ],
    'Construction': [
        {
            'name': 'Residential Construction',
            'description': 'Complete home building services from foundation to finishing with quality craftsmanship.',
            'base_price': Decimal('150000.00'),
        },
        {
            'name': 'Commercial Building Construction',
            'description': 'Large-scale commercial construction projects including offices, retail spaces, and warehouses.',
            'base_price': Decimal('250000.00'),
        },
        {
            'name': 'Home Extension & Addition',
            'description': 'Expand your living space with professional home extensions and room additions.',
            'base_price': Decimal('45000.00'),
        },
        {
            'name': 'Structural Renovation',
            'description': 'Major structural repairs and renovations to restore or upgrade existing buildings.',
            'base_price': Decimal('35000.00'),
        },
        {
            'name': 'Foundation Repair',
            'description': 'Expert foundation inspection, repair, and waterproofing services.',
            'base_price': Decimal('15000.00'),
        },
        {
            'name': 'Roofing & Roof Replacement',
            'description': 'Complete roofing solutions including installation, repair, and replacement.',
            'base_price': Decimal('12000.00'),
        },
    ],
    'Plumbing': [
        {
            'name': 'Emergency Plumbing Repair',
            'description': '24/7 emergency plumbing services for leaks, burst pipes, and urgent repairs.',
            'base_price': Decimal('150.00'),
        },
        {
            'name': 'Water Heater Installation',
            'description': 'Professional water heater installation and replacement services for all types.',
            'base_price': Decimal('1200.00'),
        },
        {
            'name': 'Bathroom Plumbing',
            'description': 'Complete bathroom plumbing including fixtures, pipes, and drainage systems.',
            'base_price': Decimal('2500.00'),
        },
        {
            'name': 'Kitchen Plumbing Installation',
            'description': 'Kitchen sink, dishwasher, and appliance plumbing installation and repair.',
            'base_price': Decimal('800.00'),
        },
        {
            'name': 'Drain Cleaning & Unclogging',
            'description': 'Professional drain cleaning services using advanced equipment and techniques.',
            'base_price': Decimal('200.00'),
        },
        {
            'name': 'Pipe Repair & Replacement',
            'description': 'Pipe leak detection, repair, and full replacement services for all plumbing systems.',
            'base_price': Decimal('650.00'),
        },
    ],
    'Electrical': [
        {
            'name': 'Electrical Panel Upgrade',
            'description': 'Upgrade your electrical panel to handle modern power demands safely.',
            'base_price': Decimal('2500.00'),
        },
        {
            'name': 'Home Rewiring',
            'description': 'Complete electrical rewiring for older homes to meet current safety standards.',
            'base_price': Decimal('8000.00'),
        },
        {
            'name': 'Lighting Installation',
            'description': 'Indoor and outdoor lighting installation including LED, recessed, and decorative fixtures.',
            'base_price': Decimal('500.00'),
        },
        {
            'name': 'Electrical Outlet Installation',
            'description': 'Install new outlets, USB ports, and specialized electrical connections.',
            'base_price': Decimal('150.00'),
        },
        {
            'name': 'Smart Home Electrical Setup',
            'description': 'Smart home automation electrical installation for lighting, security, and climate control.',
            'base_price': Decimal('3500.00'),
        },
        {
            'name': 'Generator Installation',
            'description': 'Backup generator installation and connection for uninterrupted power supply.',
            'base_price': Decimal('5000.00'),
        },
    ],
    'Painting': [
        {
            'name': 'Interior House Painting',
            'description': 'Professional interior painting for walls, ceilings, and trim with premium paints.',
            'base_price': Decimal('1500.00'),
        },
        {
            'name': 'Exterior House Painting',
            'description': 'Weather-resistant exterior painting to protect and beautify your home.',
            'base_price': Decimal('3500.00'),
        },
        {
            'name': 'Cabinet Painting & Refinishing',
            'description': 'Transform kitchen and bathroom cabinets with professional painting and refinishing.',
            'base_price': Decimal('1200.00'),
        },
        {
            'name': 'Wallpaper Installation',
            'description': 'Expert wallpaper installation and removal for residential and commercial spaces.',
            'base_price': Decimal('800.00'),
        },
        {
            'name': 'Deck & Fence Staining',
            'description': 'Protect and enhance outdoor wood structures with professional staining services.',
            'base_price': Decimal('900.00'),
        },
        {
            'name': 'Commercial Painting',
            'description': 'Large-scale commercial painting projects for offices, retail spaces, and buildings.',
            'base_price': Decimal('5000.00'),
        },
    ],
    'Carpentry': [
        {
            'name': 'Custom Furniture Building',
            'description': 'Handcrafted custom furniture designed and built to your specifications.',
            'base_price': Decimal('2000.00'),
        },
        {
            'name': 'Kitchen Cabinet Installation',
            'description': 'Professional installation of custom or pre-made kitchen cabinets.',
            'base_price': Decimal('3500.00'),
        },
        {
            'name': 'Deck Building & Repair',
            'description': 'Custom deck construction and repair services using quality materials.',
            'base_price': Decimal('4500.00'),
        },
        {
            'name': 'Door & Window Installation',
            'description': 'Expert installation of interior and exterior doors and windows.',
            'base_price': Decimal('800.00'),
        },
        {
            'name': 'Crown Molding & Trim Work',
            'description': 'Elegant crown molding, baseboards, and decorative trim installation.',
            'base_price': Decimal('1200.00'),
        },
        {
            'name': 'Shelving & Storage Solutions',
            'description': 'Custom built-in shelving and storage solutions for any room.',
            'base_price': Decimal('1500.00'),
        },
    ],
    'HVAC': [
        {
            'name': 'Central AC Installation',
            'description': 'Complete central air conditioning system installation for whole-home cooling.',
            'base_price': Decimal('6500.00'),
        },
        {
            'name': 'Furnace Installation & Repair',
            'description': 'Professional furnace installation, repair, and maintenance services.',
            'base_price': Decimal('4500.00'),
        },
        {
            'name': 'Ductwork Installation',
            'description': 'New ductwork installation and existing duct repair and sealing.',
            'base_price': Decimal('3000.00'),
        },
        {
            'name': 'Heat Pump Installation',
            'description': 'Energy-efficient heat pump installation for heating and cooling.',
            'base_price': Decimal('7000.00'),
        },
        {
            'name': 'HVAC Maintenance Service',
            'description': 'Seasonal HVAC maintenance to keep your system running efficiently.',
            'base_price': Decimal('200.00'),
        },
        {
            'name': 'Air Quality Improvement',
            'description': 'Indoor air quality solutions including filtration, humidification, and purification.',
            'base_price': Decimal('1500.00'),
        },
    ],
    'Landscaping': [
        {
            'name': 'Lawn Care & Maintenance',
            'description': 'Regular lawn mowing, edging, fertilizing, and seasonal maintenance.',
            'base_price': Decimal('150.00'),
        },
        {
            'name': 'Garden Design & Installation',
            'description': 'Custom garden design and planting for beautiful outdoor spaces.',
            'base_price': Decimal('2500.00'),
        },
        {
            'name': 'Hardscaping & Patio Installation',
            'description': 'Stone patios, walkways, retaining walls, and outdoor living spaces.',
            'base_price': Decimal('5500.00'),
        },
        {
            'name': 'Tree & Shrub Planting',
            'description': 'Professional tree and shrub selection, planting, and establishment.',
            'base_price': Decimal('800.00'),
        },
        {
            'name': 'Irrigation System Installation',
            'description': 'Automated sprinkler and drip irrigation system design and installation.',
            'base_price': Decimal('3500.00'),
        },
        {
            'name': 'Outdoor Lighting Design',
            'description': 'Landscape lighting to enhance beauty and security of outdoor spaces.',
            'base_price': Decimal('2000.00'),
        },
    ],
    'Roofing': [
        {
            'name': 'Asphalt Shingle Roofing',
            'description': 'Durable asphalt shingle roof installation with warranty protection.',
            'base_price': Decimal('8500.00'),
        },
        {
            'name': 'Metal Roofing Installation',
            'description': 'Long-lasting metal roof installation for residential and commercial buildings.',
            'base_price': Decimal('12000.00'),
        },
        {
            'name': 'Roof Leak Repair',
            'description': 'Fast and effective roof leak detection and repair services.',
            'base_price': Decimal('500.00'),
        },
        {
            'name': 'Flat Roof Installation',
            'description': 'Commercial flat roofing systems including TPO, EPDM, and modified bitumen.',
            'base_price': Decimal('9500.00'),
        },
        {
            'name': 'Gutter Installation & Repair',
            'description': 'Seamless gutter installation and repair to protect your foundation.',
            'base_price': Decimal('1200.00'),
        },
        {
            'name': 'Roof Inspection & Maintenance',
            'description': 'Comprehensive roof inspection and preventive maintenance services.',
            'base_price': Decimal('300.00'),
        },
    ],
    'Flooring': [
        {
            'name': 'Hardwood Floor Installation',
            'description': 'Beautiful solid or engineered hardwood flooring installation.',
            'base_price': Decimal('4500.00'),
        },
        {
            'name': 'Tile Flooring Installation',
            'description': 'Ceramic, porcelain, or natural stone tile flooring installation.',
            'base_price': Decimal('3500.00'),
        },
        {
            'name': 'Laminate Flooring Installation',
            'description': 'Affordable and durable laminate flooring installation.',
            'base_price': Decimal('2500.00'),
        },
        {
            'name': 'Vinyl & LVP Installation',
            'description': 'Luxury vinyl plank and sheet vinyl flooring installation.',
            'base_price': Decimal('3000.00'),
        },
        {
            'name': 'Floor Refinishing',
            'description': 'Restore hardwood floors with professional sanding and refinishing.',
            'base_price': Decimal('2800.00'),
        },
        {
            'name': 'Carpet Installation',
            'description': 'Wall-to-wall carpet installation with quality padding and materials.',
            'base_price': Decimal('2000.00'),
        },
    ],
}

def add_services():
    # Get the first available provider
    provider = Provider.objects.first()
    
    if not provider:
        print("✗ No provider found in database. Please create a provider first.")
        return
    
    print(f"✓ Using provider: {provider.business_name}")
    
    total_added = 0
    
    for category_name, services_list in services_data.items():
        try:
            category = Category.objects.get(name=category_name)
            print(f"\n{'='*60}")
            print(f"Category: {category_name}")
            print(f"{'='*60}")
            
            for service_data in services_list:
                # Check if service already exists
                existing = Service.objects.filter(
                    name=service_data['name'],
                    category=category
                ).first()
                
                if existing:
                    print(f"  ⊘ Skipped: {service_data['name']} (already exists)")
                else:
                    service = Service.objects.create(
                        category=category,
                        provider=provider,
                        name=service_data['name'],
                        description=service_data['description'],
                        base_price=service_data['base_price'],
                        is_active=True,
                    )
                    print(f"  ✓ Added: {service_data['name']} (£{service_data['base_price']})")
                    total_added += 1
            
            # Show final count for this category
            total_services = Service.objects.filter(category=category).count()
            print(f"  → Total services in {category_name}: {total_services}")
            
        except Category.DoesNotExist:
            print(f"✗ Category '{category_name}' not found. Skipping...")
    
    print(f"\n{'='*60}")
    print(f"✓ COMPLETE: Added {total_added} new services")
    print(f"{'='*60}")
    
    # Summary
    print("\n📊 FINAL SUMMARY:")
    print(f"{'='*60}")
    for category in Category.objects.all():
        service_count = Service.objects.filter(category=category).count()
        status = "✓" if service_count >= 6 else "⚠"
        print(f"{status} {category.name}: {service_count} services")

if __name__ == '__main__':
    add_services()
