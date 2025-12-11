"""
Management command to populate services with related data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import time
from categories.models import Category, SubCategory
from services.models import (
    Service, AdditionalImage, SubService, 
    ServiceInclude, ServiceFAQ, BusinessHours
)
from providers.models import Provider

User = get_user_model()


class Command(BaseCommand):
    help = 'Delete all service data and populate with realistic data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting all existing service data...'))
        
        # Delete all services and related data
        Service.objects.all().delete()
        Category.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ All service data deleted'))
        
        # Create or get providers
        self.stdout.write(self.style.WARNING('\nCreating providers...'))
        providers = []
        providers_data = [
            {'business_name': 'Elite Electrical Solutions', 'email': 'contact@eliteelectric.com', 'phone': '+1-555-0101', 'city': 'Los Angeles', 'address': '123 Electric Ave, Los Angeles, CA 90001', 'postal_code': '90001'},
            {'business_name': 'Pro Plumbing Services', 'email': 'info@proplumbing.com', 'phone': '+1-555-0202', 'city': 'San Francisco', 'address': '456 Plumber St, San Francisco, CA 94102', 'postal_code': '94102'},
            {'business_name': 'Sparkle Clean Co', 'email': 'hello@sparkleclean.com', 'phone': '+1-555-0303', 'city': 'San Diego', 'address': '789 Clean Blvd, San Diego, CA 92101', 'postal_code': '92101'},
            {'business_name': 'BuildRight Construction', 'email': 'contact@buildright.com', 'phone': '+1-555-0404', 'city': 'Sacramento', 'address': '321 Builder Rd, Sacramento, CA 95814', 'postal_code': '95814'},
            {'business_name': 'AutoCare Services', 'email': 'info@autocare.com', 'phone': '+1-555-0505', 'city': 'Oakland', 'address': '654 Auto Way, Oakland, CA 94601', 'postal_code': '94601'},
            {'business_name': 'Design Masters', 'email': 'hello@designmasters.com', 'phone': '+1-555-0606', 'city': 'Fresno', 'address': '987 Design Ave, Fresno, CA 93701', 'postal_code': '93701'},
        ]
        
        for idx, provider_data in enumerate(providers_data, 1):
            # Create or get user for provider
            user, created = User.objects.get_or_create(
                username=f'provider{idx}',
                defaults={
                    'email': provider_data['email'],
                    'first_name': provider_data['business_name'].split()[0],
                    'last_name': 'Provider',
                }
            )
            
            # Create or get provider
            provider, created = Provider.objects.get_or_create(
                user=user,
                defaults={
                    **provider_data,
                    'bio': f'Professional {provider_data["business_name"]} with years of experience',
                    'is_verified': True,
                    'rating': round(4.5 + (idx * 0.1), 1),
                    'total_reviews': 50 + (idx * 20),
                    'is_active': True,
                }
            )
            providers.append(provider)
            self.stdout.write(f'  ✓ Created provider: {provider.business_name}')
        
        # Create Categories
        self.stdout.write(self.style.WARNING('\nCreating categories...'))
        categories_data = [
            {'name': 'Electrical Services', 'description': 'Professional electrical installation and repair services', 'is_featured': True, 'order': 1},
            {'name': 'Plumbing Services', 'description': 'Expert plumbing solutions for homes and businesses', 'is_featured': True, 'order': 2},
            {'name': 'Cleaning Services', 'description': 'Professional cleaning services for residential and commercial spaces', 'is_featured': True, 'order': 3},
            {'name': 'Construction', 'description': 'Building construction and renovation services', 'is_featured': True, 'order': 4},
            {'name': 'Car Services', 'description': 'Complete car maintenance and repair services', 'is_featured': False, 'order': 5},
            {'name': 'Interior Design', 'description': 'Professional interior design and decoration', 'is_featured': False, 'order': 6},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories[cat_data['name']] = category
            self.stdout.write(f'  ✓ Created category: {category.name}')
        
        # Create SubCategories
        self.stdout.write(self.style.WARNING('\nCreating subcategories...'))
        subcategories_data = [
            {'category': 'Electrical Services', 'name': 'Installation', 'order': 1},
            {'category': 'Electrical Services', 'name': 'Repair & Maintenance', 'order': 2},
            {'category': 'Plumbing Services', 'name': 'Pipe Installation', 'order': 1},
            {'category': 'Plumbing Services', 'name': 'Leak Repair', 'order': 2},
            {'category': 'Cleaning Services', 'name': 'House Cleaning', 'order': 1},
            {'category': 'Cleaning Services', 'name': 'Office Cleaning', 'order': 2},
            {'category': 'Construction', 'name': 'Residential', 'order': 1},
            {'category': 'Construction', 'name': 'Commercial', 'order': 2},
            {'category': 'Car Services', 'name': 'Car Wash', 'order': 1},
            {'category': 'Car Services', 'name': 'Car Repair', 'order': 2},
            {'category': 'Interior Design', 'name': 'Home Interior', 'order': 1},
            {'category': 'Interior Design', 'name': 'Office Interior', 'order': 2},
        ]
        
        subcategories = {}
        for subcat_data in subcategories_data:
            cat_name = subcat_data.pop('category')
            subcategory = SubCategory.objects.create(
                category=categories[cat_name],
                **subcat_data
            )
            subcategories[f"{cat_name}_{subcat_data['name']}"] = subcategory
            self.stdout.write(f'  ✓ Created subcategory: {subcategory.name}')
        
        # Create Services with all related data
        self.stdout.write(self.style.WARNING('\nCreating services with related data...'))
        
        services_data = [
            {
                'category': 'Electrical Services',
                'subcategory': 'Electrical Services_Installation',
                'name': 'Complete Home Electrical Installation',
                'short_description': 'Professional electrical wiring and installation for new homes and renovations',
                'overview': 'Our comprehensive electrical installation service covers everything from initial planning to final inspection. We provide expert installation of wiring, switches, outlets, lighting fixtures, and electrical panels. Our certified electricians ensure all work meets safety standards and building codes.',
                'rating': 4.8,
                'total_reviews': 145,
                'services_provided': 289,
                'views_count': 1250,
                'is_featured': True,
                'is_popular': True,
                'sub_services': [
                    {'name': 'Ceiling Fan Installation', 'description': 'Professional ceiling fan installation service', 'icon': 'ti-air-conditioning', 'price': 45.00, 'duration': 60, 'alt_text': 'Ceiling fan installation service'},
                    {'name': 'Light Fixture Installation', 'description': 'Install modern lighting fixtures', 'icon': 'feather-sun', 'price': 35.00, 'duration': 45, 'alt_text': 'Light fixture installation'},
                    {'name': 'Outlet & Switch Installation', 'description': 'Install new outlets and switches', 'icon': 'feather-power', 'price': 25.00, 'duration': 30, 'alt_text': 'Outlet and switch installation'},
                    {'name': 'Electrical Panel Upgrade', 'description': 'Upgrade electrical panel for higher capacity', 'icon': 'feather-box', 'price': 150.00, 'duration': 120, 'alt_text': 'Electrical panel upgrade service'},
                ],
                'includes': [
                    {'title': 'Free Consultation', 'icon': 'feather-message-circle'},
                    {'title': '1 Year Warranty', 'icon': 'feather-shield'},
                    {'title': 'Licensed Electricians', 'icon': 'feather-award'},
                    {'title': 'Safety Inspection', 'icon': 'feather-check-circle'},
                ],
                'faqs': [
                    {'question': 'Do you provide emergency electrical services?', 'answer': 'Yes, we offer 24/7 emergency electrical services for urgent issues.'},
                    {'question': 'Are your electricians licensed?', 'answer': 'All our electricians are fully licensed, insured, and certified professionals.'},
                    {'question': 'What is your warranty policy?', 'answer': 'We provide a 1-year warranty on all electrical installation work.'},
                ],
            },
            {
                'category': 'Plumbing Services',
                'subcategory': 'Plumbing Services_Leak Repair',
                'name': 'Emergency Plumbing & Leak Repair',
                'short_description': '24/7 emergency plumbing services for leaks, burst pipes, and drainage issues',
                'overview': 'Fast and reliable emergency plumbing service available round the clock. Our experienced plumbers handle all types of leaks, from minor drips to major burst pipes. We use advanced leak detection equipment and provide permanent solutions, not just temporary fixes.',
                'rating': 4.9,
                'total_reviews': 203,
                'services_provided': 456,
                'views_count': 1890,
                'is_featured': True,
                'is_popular': True,
                'sub_services': [
                    {'name': 'Pipe Leak Detection', 'description': 'Advanced leak detection with modern equipment', 'icon': 'feather-droplet', 'price': 75.00, 'duration': 45, 'alt_text': 'Pipe leak detection service'},
                    {'name': 'Burst Pipe Repair', 'description': 'Emergency burst pipe repair service', 'icon': 'feather-alert-circle', 'price': 125.00, 'duration': 90, 'alt_text': 'Burst pipe repair'},
                    {'name': 'Faucet Repair', 'description': 'Fix dripping and faulty faucets', 'icon': 'feather-tool', 'price': 40.00, 'duration': 30, 'alt_text': 'Faucet repair service'},
                    {'name': 'Drain Cleaning', 'description': 'Professional drain cleaning and unclogging', 'icon': 'feather-filter', 'price': 85.00, 'duration': 60, 'alt_text': 'Drain cleaning service'},
                ],
                'includes': [
                    {'title': '24/7 Availability', 'icon': 'feather-clock'},
                    {'title': 'Fast Response Time', 'icon': 'feather-zap'},
                    {'title': 'Expert Plumbers', 'icon': 'feather-users'},
                    {'title': 'Quality Parts', 'icon': 'feather-package'},
                ],
                'faqs': [
                    {'question': 'How quickly can you respond to emergencies?', 'answer': 'We typically arrive within 1-2 hours for emergency calls.'},
                    {'question': 'Do you offer same-day service?', 'answer': 'Yes, we provide same-day service for most plumbing issues.'},
                    {'question': 'What payment methods do you accept?', 'answer': 'We accept cash, credit cards, and digital payments.'},
                ],
            },
            {
                'category': 'Cleaning Services',
                'subcategory': 'Cleaning Services_House Cleaning',
                'name': 'Deep House Cleaning Service',
                'short_description': 'Thorough deep cleaning for homes with attention to every detail',
                'overview': 'Our deep house cleaning service goes beyond regular cleaning. We clean every corner, surface, and hidden area of your home. Our trained professionals use eco-friendly products and advanced equipment to ensure a spotless, healthy living environment.',
                'rating': 4.7,
                'total_reviews': 312,
                'services_provided': 678,
                'views_count': 2340,
                'is_featured': True,
                'is_popular': True,
                'sub_services': [
                    {'name': 'Kitchen Deep Clean', 'description': 'Thorough kitchen cleaning including appliances', 'icon': 'feather-home', 'price': 65.00, 'duration': 90, 'alt_text': 'Kitchen deep cleaning service'},
                    {'name': 'Bathroom Sanitization', 'description': 'Complete bathroom sanitization and cleaning', 'icon': 'feather-droplet', 'price': 50.00, 'duration': 60, 'alt_text': 'Bathroom sanitization'},
                    {'name': 'Floor Cleaning', 'description': 'Professional floor cleaning all types', 'icon': 'feather-square', 'price': 45.00, 'duration': 45, 'alt_text': 'Floor cleaning service'},
                    {'name': 'Window Cleaning', 'description': 'Streak-free window cleaning service', 'icon': 'feather-wind', 'price': 40.00, 'duration': 40, 'alt_text': 'Window cleaning service'},
                ],
                'includes': [
                    {'title': 'Eco-Friendly Products', 'icon': 'feather-leaf'},
                    {'title': 'Professional Equipment', 'icon': 'feather-tool'},
                    {'title': 'Trained Staff', 'icon': 'feather-award'},
                    {'title': 'Satisfaction Guarantee', 'icon': 'feather-check'},
                ],
                'faqs': [
                    {'question': 'How long does deep cleaning take?', 'answer': 'Typically 4-6 hours depending on home size and condition.'},
                    {'question': 'Do I need to provide cleaning supplies?', 'answer': 'No, we bring all necessary supplies and equipment.'},
                    {'question': 'Can I schedule recurring cleaning?', 'answer': 'Yes, we offer weekly, bi-weekly, and monthly cleaning plans.'},
                ],
            },
            {
                'category': 'Construction',
                'subcategory': 'Construction_Residential',
                'name': 'Home Renovation & Remodeling',
                'short_description': 'Complete home renovation services from planning to completion',
                'overview': 'Transform your home with our comprehensive renovation services. We handle everything from kitchen and bathroom remodels to complete home makeovers. Our team includes architects, designers, and skilled craftsmen who work together to bring your vision to life.',
                'rating': 4.6,
                'total_reviews': 89,
                'services_provided': 124,
                'views_count': 987,
                'is_featured': False,
                'is_popular': True,
                'sub_services': [
                    {'name': 'Kitchen Remodeling', 'description': 'Complete kitchen renovation and remodeling', 'icon': 'feather-home', 'price': 350.00, 'duration': 180, 'alt_text': 'Kitchen remodeling service'},
                    {'name': 'Bathroom Renovation', 'description': 'Full bathroom renovation service', 'icon': 'feather-droplet', 'price': 280.00, 'duration': 150, 'alt_text': 'Bathroom renovation'},
                    {'name': 'Room Addition', 'description': 'Add new rooms to your home', 'icon': 'feather-plus-square', 'price': 500.00, 'duration': 300, 'alt_text': 'Room addition service'},
                    {'name': 'Flooring Installation', 'description': 'Professional flooring installation service', 'icon': 'feather-layers', 'price': 200.00, 'duration': 120, 'alt_text': 'Flooring installation'},
                ],
                'includes': [
                    {'title': '3D Design Preview', 'icon': 'feather-eye'},
                    {'title': 'Project Management', 'icon': 'feather-clipboard'},
                    {'title': 'Quality Materials', 'icon': 'feather-package'},
                    {'title': 'Timeline Guarantee', 'icon': 'feather-calendar'},
                ],
                'faqs': [
                    {'question': 'Do you handle permits?', 'answer': 'Yes, we manage all necessary permits and inspections.'},
                    {'question': 'What is the typical timeline?', 'answer': 'Projects typically take 4-12 weeks depending on scope.'},
                    {'question': 'Do you offer financing?', 'answer': 'Yes, we have flexible payment and financing options.'},
                ],
            },
            {
                'category': 'Car Services',
                'subcategory': 'Car Services_Car Wash',
                'name': 'Premium Car Wash & Detailing',
                'short_description': 'Professional car washing and detailing services with premium products',
                'overview': 'Give your car the care it deserves with our premium car wash and detailing service. We use high-quality products and techniques to clean, polish, and protect your vehicle. From exterior wash to interior detailing, we ensure your car looks and feels brand new.',
                'rating': 4.5,
                'total_reviews': 267,
                'services_provided': 1234,
                'views_count': 3456,
                'is_featured': False,
                'is_popular': False,
                'sub_services': [
                    {'name': 'Exterior Wash & Wax', 'description': 'Complete exterior car wash and waxing', 'icon': 'feather-droplet', 'price': 55.00, 'duration': 60, 'alt_text': 'Exterior car wash and wax'},
                    {'name': 'Interior Detailing', 'description': 'Deep interior cleaning and detailing', 'icon': 'feather-home', 'price': 75.00, 'duration': 90, 'alt_text': 'Interior car detailing'},
                    {'name': 'Engine Cleaning', 'description': 'Professional engine bay cleaning', 'icon': 'feather-tool', 'price': 45.00, 'duration': 45, 'alt_text': 'Engine cleaning service'},
                    {'name': 'Paint Protection', 'description': 'Ceramic coating and paint protection', 'icon': 'feather-shield', 'price': 150.00, 'duration': 120, 'alt_text': 'Car paint protection'},
                ],
                'includes': [
                    {'title': 'Premium Products', 'icon': 'feather-star'},
                    {'title': 'Hand Wash', 'icon': 'feather-hand'},
                    {'title': 'Vacuum Cleaning', 'icon': 'feather-wind'},
                    {'title': 'Tire Shine', 'icon': 'feather-circle'},
                ],
                'faqs': [
                    {'question': 'How long does a full detail take?', 'answer': 'A complete detail typically takes 3-4 hours.'},
                    {'question': 'Do you offer mobile service?', 'answer': 'Yes, we can come to your location for detailing.'},
                    {'question': 'What products do you use?', 'answer': 'We use premium, eco-friendly car care products.'},
                ],
            },
            {
                'category': 'Interior Design',
                'subcategory': 'Interior Design_Home Interior',
                'name': 'Modern Home Interior Design',
                'short_description': 'Contemporary interior design services for stylish and functional homes',
                'overview': 'Create your dream home with our modern interior design services. Our expert designers work closely with you to understand your style preferences and create spaces that are both beautiful and functional. We handle everything from concept to execution.',
                'rating': 4.9,
                'total_reviews': 156,
                'services_provided': 234,
                'views_count': 1567,
                'is_featured': True,
                'is_popular': False,
                'sub_services': [
                    {'name': 'Living Room Design', 'description': 'Modern living room interior design', 'icon': 'feather-home', 'price': 180.00, 'duration': 120, 'alt_text': 'Living room design service'},
                    {'name': 'Bedroom Design', 'description': 'Comfortable bedroom interior design', 'icon': 'feather-moon', 'price': 160.00, 'duration': 100, 'alt_text': 'Bedroom design'},
                    {'name': 'Kitchen Design', 'description': 'Functional kitchen interior design', 'icon': 'feather-coffee', 'price': 200.00, 'duration': 130, 'alt_text': 'Kitchen design service'},
                    {'name': 'Color Consultation', 'description': 'Professional color scheme consultation', 'icon': 'feather-droplet', 'price': 95.00, 'duration': 60, 'alt_text': 'Color consultation'},
                ],
                'includes': [
                    {'title': '3D Visualization', 'icon': 'feather-eye'},
                    {'title': 'Furniture Selection', 'icon': 'feather-shopping-bag'},
                    {'title': 'Project Supervision', 'icon': 'feather-users'},
                    {'title': 'Budget Planning', 'icon': 'feather-dollar-sign'},
                ],
                'faqs': [
                    {'question': 'Do you work within a budget?', 'answer': 'Yes, we create designs that match your budget requirements.'},
                    {'question': 'Can I see designs before work starts?', 'answer': 'Yes, we provide detailed 3D visualizations for approval.'},
                    {'question': 'How long does the design process take?', 'answer': 'Design phase typically takes 2-4 weeks.'},
                ],
            },
        ]
        
        # Business hours template (Monday-Saturday 9:30 AM - 7:00 PM, Sunday Closed)
        business_hours_template = [
            {'weekday': 0, 'opening_time': time(9, 30), 'closing_time': time(19, 0), 'is_closed': False},
            {'weekday': 1, 'opening_time': time(9, 30), 'closing_time': time(19, 0), 'is_closed': False},
            {'weekday': 2, 'opening_time': time(9, 30), 'closing_time': time(19, 0), 'is_closed': False},
            {'weekday': 3, 'opening_time': time(9, 30), 'closing_time': time(19, 0), 'is_closed': False},
            {'weekday': 4, 'opening_time': time(9, 30), 'closing_time': time(19, 0), 'is_closed': False},
            {'weekday': 5, 'opening_time': time(9, 30), 'closing_time': time(19, 0), 'is_closed': False},
            {'weekday': 6, 'opening_time': None, 'closing_time': None, 'is_closed': True},
        ]
        
        # Create services
        for idx, service_data in enumerate(services_data):
            # Extract related data
            sub_services = service_data.pop('sub_services', [])
            includes = service_data.pop('includes', [])
            faqs = service_data.pop('faqs', [])
            
            # Get category and subcategory
            cat_name = service_data.pop('category')
            subcat_key = service_data.pop('subcategory')
            
            # Assign provider (cycle through providers)
            provider = providers[idx % len(providers)]
            
            # Create service
            service = Service.objects.create(
                category=categories[cat_name],
                subcategory=subcategories.get(subcat_key),
                provider=provider,
                **service_data
            )
            
            self.stdout.write(f'\n  ✓ Created service: {service.name}')
            
            # Create sub-services
            for idx, sub_service_data in enumerate(sub_services, 1):
                SubService.objects.create(
                    service=service,
                    order=idx,
                    is_active=True,
                    **sub_service_data
                )
            self.stdout.write(f'    → Added {len(sub_services)} sub-services')
            
            # Create includes
            for idx, include_data in enumerate(includes, 1):
                ServiceInclude.objects.create(
                    service=service,
                    order=idx,
                    **include_data
                )
            self.stdout.write(f'    → Added {len(includes)} service includes')
            
            # Create FAQs
            for idx, faq_data in enumerate(faqs, 1):
                ServiceFAQ.objects.create(
                    service=service,
                    order=idx,
                    is_active=True,
                    **faq_data
                )
            self.stdout.write(f'    → Added {len(faqs)} FAQs')
            
            # Create business hours
            for hours_data in business_hours_template:
                BusinessHours.objects.create(
                    service=service,
                    **hours_data
                )
            self.stdout.write(f'    → Added business hours (Mon-Sat: 9:30 AM - 7:00 PM, Sun: Closed)')
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('DATA POPULATION COMPLETED'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'✓ Categories created: {Category.objects.count()}')
        self.stdout.write(f'✓ SubCategories created: {SubCategory.objects.count()}')
        self.stdout.write(f'✓ Services created: {Service.objects.count()}')
        self.stdout.write(f'✓ Sub-services created: {SubService.objects.count()}')
        self.stdout.write(f'✓ Service includes created: {ServiceInclude.objects.count()}')
        self.stdout.write(f'✓ Service FAQs created: {ServiceFAQ.objects.count()}')
        self.stdout.write(f'✓ Business hours created: {BusinessHours.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*60))
