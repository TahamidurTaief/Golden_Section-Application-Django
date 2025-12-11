"""
Management command to populate services with related data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
from categories.models import Category, SubCategory
from services.models import (
    Service, AdditionalImage, SubService, 
    ServiceInclude, ServiceFAQ, BusinessHours
)


class Command(BaseCommand):
    help = 'Delete all service data and populate with realistic data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting all existing service data...'))
        
        # Delete all services and related data
        Service.objects.all().delete()
        Category.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('✓ All service data deleted'))
        
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
                    {'name': 'Ceiling Fan Installation', 'icon': 'ti-air-conditioning'},
                    {'name': 'Light Fixture Installation', 'icon': 'feather-sun'},
                    {'name': 'Outlet & Switch Installation', 'icon': 'feather-power'},
                    {'name': 'Electrical Panel Upgrade', 'icon': 'feather-box'},
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
                    {'name': 'Pipe Leak Detection', 'icon': 'feather-droplet'},
                    {'name': 'Burst Pipe Repair', 'icon': 'feather-alert-circle'},
                    {'name': 'Faucet Repair', 'icon': 'feather-tool'},
                    {'name': 'Drain Cleaning', 'icon': 'feather-filter'},
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
                    {'name': 'Kitchen Deep Clean', 'icon': 'feather-home'},
                    {'name': 'Bathroom Sanitization', 'icon': 'feather-droplet'},
                    {'name': 'Floor Cleaning', 'icon': 'feather-square'},
                    {'name': 'Window Cleaning', 'icon': 'feather-wind'},
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
                    {'name': 'Kitchen Remodeling', 'icon': 'feather-home'},
                    {'name': 'Bathroom Renovation', 'icon': 'feather-droplet'},
                    {'name': 'Room Addition', 'icon': 'feather-plus-square'},
                    {'name': 'Flooring Installation', 'icon': 'feather-layers'},
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
                    {'name': 'Exterior Wash & Wax', 'icon': 'feather-droplet'},
                    {'name': 'Interior Detailing', 'icon': 'feather-home'},
                    {'name': 'Engine Cleaning', 'icon': 'feather-tool'},
                    {'name': 'Paint Protection', 'icon': 'feather-shield'},
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
                    {'name': 'Living Room Design', 'icon': 'feather-home'},
                    {'name': 'Bedroom Design', 'icon': 'feather-moon'},
                    {'name': 'Kitchen Design', 'icon': 'feather-coffee'},
                    {'name': 'Color Consultation', 'icon': 'feather-droplet'},
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
        for service_data in services_data:
            # Extract related data
            sub_services = service_data.pop('sub_services', [])
            includes = service_data.pop('includes', [])
            faqs = service_data.pop('faqs', [])
            
            # Get category and subcategory
            cat_name = service_data.pop('category')
            subcat_key = service_data.pop('subcategory')
            
            # Create service
            service = Service.objects.create(
                category=categories[cat_name],
                subcategory=subcategories.get(subcat_key),
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
