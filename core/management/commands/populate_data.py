from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from accounts.models import User
from site_config.models import SiteConfiguration, ImportantLink
from categories.models import Category, SubCategory
from services.models import Service, ServicePricingTier, ServiceGallery
from providers.models import Provider, ProviderGallery, ProviderReview
from content.models import Page, FAQ, Testimonial, BlogPost
from quotations.models import ServiceRequest


class Command(BaseCommand):
    help = 'Populate database with fake data for development'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database with fake data...\n')
        
        # Create site configuration
        self.create_site_config()
        
        # Create users
        users = self.create_users()
        
        # Create categories and subcategories
        categories = self.create_categories()
        
        # Create services with pricing tiers
        services = self.create_services(categories)
        
        # Create providers
        providers = self.create_providers(users['providers'], services, categories)
        
        # Create content
        self.create_pages()
        self.create_faqs(categories)
        self.create_testimonials(services)
        self.create_blog_posts(users['admins'], categories)
        
        # Create service requests
        self.create_service_requests(users['customers'], services)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS('   - Site configuration created'))
        self.stdout.write(self.style.SUCCESS('   - 20+ users created'))
        self.stdout.write(self.style.SUCCESS('   - 8 categories with subcategories'))
        self.stdout.write(self.style.SUCCESS('   - 24+ services with pricing tiers'))
        self.stdout.write(self.style.SUCCESS('   - 10 providers with reviews'))
        self.stdout.write(self.style.SUCCESS('   - Static pages, FAQs, testimonials'))
        self.stdout.write(self.style.SUCCESS('   - Blog posts and service requests'))

    def create_site_config(self):
        self.stdout.write('Creating site configuration...')
        config = SiteConfiguration.load()
        config.site_name = 'Golden Section'
        config.site_tagline = 'Your Trusted Service Provider'
        config.primary_email = 'info@goldensection.com'
        config.primary_phone = '+44 20 7123 4567'
        config.default_whatsapp = '+44 7700 900000'
        config.address = '123 Oxford Street, London, W1D 2HG, United Kingdom'
        config.meta_title = 'Golden Section - Professional Services in London'
        config.meta_description = 'Find trusted professionals for home services, cleaning, moving, repairs and more in London.'
        config.meta_keywords = 'home services, cleaning, moving, repairs, london'
        config.facebook_url = 'https://facebook.com/goldensection'
        config.twitter_url = 'https://twitter.com/goldensection'
        config.instagram_url = 'https://instagram.com/goldensection'
        config.linkedin_url = 'https://linkedin.com/company/goldensection'
        config.google_analytics_id = 'G-XXXXXXXXXX'
        config.facebook_pixel_id = '123456789012345'
        config.footer_description = 'Golden Section connects you with trusted service providers for all your home and business needs.'
        config.copyright_text = '© 2025 Golden Section. All rights reserved.'
        config.save()
        
        # Create important links
        links = [
            ('About Us', '/pages/about/', 1),
            ('Services', '/services/', 2),
            ('Providers', '/providers/', 3),
            ('Contact', '/pages/contact/', 4),
            ('Privacy Policy', '/pages/privacy/', 5),
            ('Terms & Conditions', '/pages/terms/', 6),
        ]
        for title, url, order in links:
            ImportantLink.objects.get_or_create(
                title=title,
                defaults={'url': url, 'order': order, 'is_active': True}
            )

    def create_users(self):
        self.stdout.write('Creating users...')
        
        # Create admin users
        admins = []
        for i in range(2):
            user, created = User.objects.get_or_create(
                username=f'admin{i+1}',
                defaults={
                    'email': f'admin{i+1}@goldensection.com',
                    'first_name': ['John', 'Sarah'][i],
                    'last_name': ['Smith', 'Johnson'][i],
                    'role': 'admin',
                    'is_staff': True,
                    'is_superuser': True,
                    'phone': f'+44 7700 90000{i}',
                    'city': 'London',
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('admin123')
                user.save()
            admins.append(user)
        
        # Create provider users
        providers = []
        provider_names = [
            ('Michael', 'Brown'), ('Emma', 'Wilson'), ('James', 'Taylor'),
            ('Olivia', 'Anderson'), ('William', 'Thomas'), ('Sophia', 'Jackson'),
            ('Robert', 'White'), ('Isabella', 'Harris'), ('David', 'Martin'),
            ('Charlotte', 'Thompson')
        ]
        for i, (first, last) in enumerate(provider_names):
            user, created = User.objects.get_or_create(
                username=f'provider{i+1}',
                defaults={
                    'email': f'{first.lower()}.{last.lower()}@example.com',
                    'first_name': first,
                    'last_name': last,
                    'role': 'provider',
                    'phone': f'+44 7700 80{i:04d}',
                    'city': random.choice(['London', 'Manchester', 'Birmingham', 'Leeds']),
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('provider123')
                user.save()
            providers.append(user)
        
        # Create customer users
        customers = []
        customer_names = [
            ('Alice', 'Davies'), ('Bob', 'Evans'), ('Carol', 'Roberts'),
            ('Daniel', 'Wright'), ('Emily', 'Walker'), ('Frank', 'Robinson'),
            ('Grace', 'Wood'), ('Henry', 'Scott')
        ]
        for i, (first, last) in enumerate(customer_names):
            user, created = User.objects.get_or_create(
                username=f'customer{i+1}',
                defaults={
                    'email': f'{first.lower()}.{last.lower()}@example.com',
                    'first_name': first,
                    'last_name': last,
                    'role': 'customer',
                    'phone': f'+44 7700 70{i:04d}',
                    'city': random.choice(['London', 'Bristol', 'Liverpool']),
                    'is_verified': True,
                }
            )
            if created:
                user.set_password('customer123')
                user.save()
            customers.append(user)
        
        return {'admins': admins, 'providers': providers, 'customers': customers}

    def create_categories(self):
        self.stdout.write('Creating categories and subcategories...')
        
        categories_data = [
            {
                'name': 'Home Cleaning',
                'description': 'Professional home cleaning services',
                'icon': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900001',
                'subcategories': ['Deep Cleaning', 'Regular Cleaning', 'Move-in/Move-out', 'Carpet Cleaning']
            },
            {
                'name': 'Removal & Moving',
                'description': 'Reliable moving and removal services',
                'icon': 'https://images.unsplash.com/photo-1600518464441-9154a4dea21b?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1600518464441-9154a4dea21b?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900002',
                'subcategories': ['House Moving', 'Office Moving', 'Storage', 'Packing Services']
            },
            {
                'name': 'Plumbing',
                'description': 'Expert plumbing repairs and installations',
                'icon': 'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900003',
                'subcategories': ['Leak Repairs', 'Drain Cleaning', 'Installation', 'Emergency Service']
            },
            {
                'name': 'Electrical',
                'description': 'Licensed electrical services',
                'icon': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900004',
                'subcategories': ['Wiring', 'Light Installation', 'Repairs', 'Safety Inspections']
            },
            {
                'name': 'Painting & Decorating',
                'description': 'Professional painting services',
                'icon': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900005',
                'subcategories': ['Interior Painting', 'Exterior Painting', 'Wallpapering', 'Commercial']
            },
            {
                'name': 'Gardening',
                'description': 'Garden maintenance and landscaping',
                'icon': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900006',
                'subcategories': ['Lawn Care', 'Landscaping', 'Tree Services', 'Garden Design']
            },
            {
                'name': 'Handyman',
                'description': 'General home repairs and maintenance',
                'icon': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900007',
                'subcategories': ['Furniture Assembly', 'Door Repairs', 'Shelf Installation', 'General Repairs']
            },
            {
                'name': 'Pest Control',
                'description': 'Professional pest control services',
                'icon': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=100&h=100&fit=crop',
                'image': 'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=800&h=600&fit=crop',
                'whatsapp': '+44 7700 900008',
                'subcategories': ['Rodent Control', 'Insect Control', 'Prevention', 'Commercial']
            }
        ]
        
        categories = []
        for idx, cat_data in enumerate(categories_data):
            category, _ = Category.objects.get_or_create(
                slug=cat_data['name'].lower().replace(' ', '-').replace('&', 'and'),
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'image': cat_data['image'],
                    'whatsapp_number': cat_data['whatsapp'],
                    'is_active': True,
                    'is_featured': idx < 4,
                    'order': idx
                }
            )
            categories.append(category)
            
            # Create subcategories
            for sub_idx, sub_name in enumerate(cat_data['subcategories']):
                SubCategory.objects.get_or_create(
                    category=category,
                    slug=f"{category.slug}-{sub_name.lower().replace(' ', '-').replace('/', '-')}",
                    defaults={
                        'name': sub_name,
                        'description': f'{sub_name} services for {cat_data["name"].lower()}',
                        'is_active': True,
                        'order': sub_idx
                    }
                )
        
        return categories

    def create_services(self, categories):
        self.stdout.write('Creating services with pricing tiers...')
        
        services_data = [
            # Home Cleaning
            ('Deep House Cleaning', 'home-cleaning', 'Complete deep cleaning for your entire home', 
             'Our professional deep cleaning service covers every corner of your home. We use eco-friendly products and the latest equipment.', 
             'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&h=800&fit=crop'),
            ('Regular Cleaning Service', 'home-cleaning', 'Weekly or bi-weekly cleaning service',
             'Keep your home spotless with our regular cleaning service. Flexible scheduling to fit your needs.',
             'https://images.unsplash.com/photo-1628177142898-93e36e4e3a50?w=1200&h=800&fit=crop'),
            ('End of Tenancy Cleaning', 'home-cleaning', 'Professional cleaning for move-out',
             'Get your deposit back with our thorough end of tenancy cleaning service.',
             'https://images.unsplash.com/photo-1585421514738-01798e348b17?w=1200&h=800&fit=crop'),
            
            # Removal & Moving
            ('House Removal Service', 'removal-and-moving', 'Complete house moving service',
             'Stress-free house moving with our experienced team. We handle packing, loading, and unpacking.',
             'https://images.unsplash.com/photo-1600518464441-9154a4dea21b?w=1200&h=800&fit=crop'),
            ('Office Relocation', 'removal-and-moving', 'Professional office moving',
             'Minimize downtime with our efficient office relocation service.',
             'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&h=800&fit=crop'),
            ('Man and Van Service', 'removal-and-moving', 'Flexible moving solution',
             'Affordable man and van service for small moves and deliveries.',
             'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=1200&h=800&fit=crop'),
            
            # Plumbing
            ('Emergency Plumbing', 'plumbing', '24/7 emergency plumbing service',
             'Fast response for burst pipes, leaks, and plumbing emergencies.',
             'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=1200&h=800&fit=crop'),
            ('Bathroom Installation', 'plumbing', 'Complete bathroom fitting',
             'Transform your bathroom with our professional installation service.',
             'https://images.unsplash.com/photo-1620626011761-996317b8d101?w=1200&h=800&fit=crop'),
            ('Boiler Repair & Service', 'plumbing', 'Boiler maintenance and repairs',
             'Keep your boiler running efficiently with our expert service.',
             'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=1200&h=800&fit=crop'),
            
            # Electrical
            ('Electrical Rewiring', 'electrical', 'Full or partial rewiring',
             'Safe and certified electrical rewiring for homes and businesses.',
             'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=1200&h=800&fit=crop'),
            ('Light Installation', 'electrical', 'Professional lighting solutions',
             'From simple fixtures to complex lighting systems.',
             'https://images.unsplash.com/photo-1513828583688-c52646db42da?w=1200&h=800&fit=crop'),
            ('Electrical Safety Check', 'electrical', 'Comprehensive safety inspection',
             'EICR certificates and safety reports for landlords.',
             'https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=1200&h=800&fit=crop'),
            
            # Painting
            ('Interior Painting', 'painting-and-decorating', 'Professional interior painting',
             'Transform your space with our expert interior painting service.',
             'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=1200&h=800&fit=crop'),
            ('Exterior Painting', 'painting-and-decorating', 'Weather-resistant exterior painting',
             'Protect and beautify your property with quality exterior paint.',
             'https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=1200&h=800&fit=crop'),
            ('Wallpaper Hanging', 'painting-and-decorating', 'Expert wallpaper installation',
             'Perfect wallpaper application for stunning results.',
             'https://images.unsplash.com/photo-1615873968403-89e068629265?w=1200&h=800&fit=crop'),
            
            # Gardening
            ('Garden Maintenance', 'gardening', 'Regular garden upkeep',
             'Keep your garden beautiful year-round with our maintenance service.',
             'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=1200&h=800&fit=crop'),
            ('Lawn Care Service', 'gardening', 'Professional lawn treatment',
             'Mowing, fertilizing, and maintaining a perfect lawn.',
             'https://images.unsplash.com/photo-1558904541-efa843a96f01?w=1200&h=800&fit=crop'),
            ('Landscaping Design', 'gardening', 'Complete garden transformation',
             'Custom landscape design and installation services.',
             'https://images.unsplash.com/photo-1599629954294-8d5e41bc3f65?w=1200&h=800&fit=crop'),
            
            # Handyman
            ('Furniture Assembly', 'handyman', 'Expert furniture assembly',
             'We assemble all types of furniture quickly and correctly.',
             'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=1200&h=800&fit=crop'),
            ('Door Installation', 'handyman', 'Door fitting and repairs',
             'Internal and external door installation and repair.',
             'https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=1200&h=800&fit=crop'),
            ('TV Wall Mounting', 'handyman', 'Professional TV mounting',
             'Safe and secure TV wall mounting service.',
             'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=1200&h=800&fit=crop'),
            
            # Pest Control
            ('Rodent Control', 'pest-control', 'Effective rodent removal',
             'Safe and humane rodent control and prevention.',
             'https://images.unsplash.com/photo-1563453392212-326f5e854473?w=1200&h=800&fit=crop'),
            ('Bed Bug Treatment', 'pest-control', 'Complete bed bug elimination',
             'Guaranteed bed bug removal with safe treatments.',
             'https://images.unsplash.com/photo-1584516150909-c43483ee7932?w=1200&h=800&fit=crop'),
            ('Ant & Insect Control', 'pest-control', 'Insect pest management',
             'Long-lasting protection against all common insects.',
             'https://images.unsplash.com/photo-1577017040065-650ee4d43339?w=1200&h=800&fit=crop'),
        ]
        
        services = []
        for idx, (name, cat_slug, short_desc, desc, image) in enumerate(services_data):
            category = Category.objects.get(slug=cat_slug)
            
            service, _ = Service.objects.get_or_create(
                slug=name.lower().replace(' ', '-').replace('&', 'and'),
                defaults={
                    'category': category,
                    'name': name,
                    'short_description': short_desc,
                    'description': desc,
                    'featured_image': image,
                    'whatsapp_number': f'+44 7700 91{idx:04d}' if idx % 3 == 0 else '',
                    'is_featured': idx % 4 == 0,
                    'is_popular': idx % 3 == 0,
                    'is_active': True,
                    'views_count': random.randint(50, 500),
                    'order': idx
                }
            )
            services.append(service)
            
            # Create pricing tiers
            base_price = random.randint(40, 100)
            tiers = [
                ('basic', 'Basic Package', base_price, 
                 'Essential service with standard features',
                 ['Service completion', 'Basic materials', '7-day guarantee']),
                ('standard', 'Standard Package', base_price * 1.5,
                 'Most popular option with enhanced features',
                 ['Priority service', 'Premium materials', '30-day guarantee', 'Free consultation']),
                ('premium', 'Premium Package', base_price * 2,
                 'Complete service with all premium features',
                 ['Same-day service', 'Premium materials', 'Lifetime guarantee', 'Free consultation', '24/7 support'])
            ]
            
            for tier_type, tier_name, price, tier_desc, features in tiers:
                ServicePricingTier.objects.get_or_create(
                    service=service,
                    tier_type=tier_type,
                    defaults={
                        'name': tier_name,
                        'price': price,
                        'description': tier_desc,
                        'features': features,
                        'is_active': True,
                        'is_recommended': tier_type == 'standard'
                    }
                )
        
        return services

    def create_providers(self, provider_users, services, categories):
        self.stdout.write('Creating providers with reviews...')
        
        providers = []
        for user in provider_users:
            provider, _ = Provider.objects.get_or_create(
                user=user,
                defaults={
                    'business_name': f'{user.first_name} {user.last_name} Services',
                    'bio': f'Professional service provider with over {random.randint(5, 15)} years of experience. Committed to quality and customer satisfaction.',
                    'phone': user.phone,
                    'whatsapp': f'+44 7700 85{random.randint(1000, 9999)}',
                    'email': user.email,
                    'address': f'{random.randint(1, 200)} High Street',
                    'city': user.city,
                    'postal_code': f'SW{random.randint(1, 20)} {random.randint(1, 9)}XX',
                    'is_verified': True,
                    'rating': round(random.uniform(4.0, 5.0), 2),
                    'total_reviews': random.randint(10, 50),
                    'total_jobs': random.randint(50, 200),
                    'total_completed_jobs': random.randint(45, 190),
                    'is_active': True,
                    'is_featured': random.choice([True, False]),
                    'is_available': True
                }
            )
            
            # Assign random services and categories
            random_services = random.sample(list(services), k=random.randint(2, 5))
            provider.services.set(random_services)
            
            related_cats = list(set([s.category for s in random_services]))
            provider.categories.set(related_cats)
            
            providers.append(provider)
        
        return providers

    def create_pages(self):
        self.stdout.write('Creating static pages...')
        
        pages_data = [
            ('about', 'About Us', 'about', 'Learn more about Golden Section and our mission to connect you with trusted service providers.'),
            ('terms', 'Terms & Conditions', 'terms-conditions', 'Our terms and conditions for using Golden Section services.'),
            ('privacy', 'Privacy Policy', 'privacy-policy', 'How we protect and use your personal information.'),
            ('contact', 'Contact Us', 'contact', 'Get in touch with our team for any questions or support.'),
        ]
        
        for page_type, title, slug, content in pages_data:
            Page.objects.get_or_create(
                page_type=page_type,
                defaults={
                    'title': title,
                    'slug': slug,
                    'content': f'<h1>{title}</h1><p>{content}</p>',
                    'is_active': True,
                    'show_in_footer': True
                }
            )

    def create_faqs(self, categories):
        self.stdout.write('Creating FAQs...')
        
        faqs = [
            ('How do I book a service?', 'Simply browse our services, select the one you need, and fill out the booking form. We\'ll contact you within 24 hours.', None, True),
            ('Are your providers insured?', 'Yes, all our verified providers carry appropriate insurance for their services.', None, True),
            ('What payment methods do you accept?', 'We accept cash, bank transfer, and major credit/debit cards.', None, True),
            ('Can I cancel or reschedule?', 'Yes, you can cancel or reschedule up to 24 hours before the appointment.', None, False),
            ('Do you offer emergency services?', 'Yes, we have 24/7 emergency services available for plumbing and electrical work.', categories[2], False),
        ]
        
        for idx, (question, answer, category, is_featured) in enumerate(faqs):
            FAQ.objects.get_or_create(
                question=question,
                defaults={
                    'answer': answer,
                    'category': category,
                    'is_active': True,
                    'is_featured': is_featured,
                    'order': idx
                }
            )

    def create_testimonials(self, services):
        self.stdout.write('Creating testimonials...')
        
        testimonials_data = [
            ('Sarah Mitchell', 'Homeowner', 'https://i.pravatar.cc/150?img=1', 
             'Excellent service! The cleaning team was professional and thorough. Highly recommend!', 5, services[0]),
            ('John Peterson', 'Business Owner', 'https://i.pravatar.cc/150?img=2',
             'Used their office moving service. Everything was handled perfectly. Will use again!', 5, services[3]),
            ('Emma Thompson', 'Landlord', 'https://i.pravatar.cc/150?img=3',
             'Fast response for emergency plumbing. Fixed the issue quickly and professionally.', 5, services[6]),
            ('David Chen', 'Homeowner', 'https://i.pravatar.cc/150?img=4',
             'Great painting job on my house exterior. Looks fantastic and was done on time.', 5, services[12]),
            ('Lisa Anderson', 'Property Manager', 'https://i.pravatar.cc/150?img=5',
             'Reliable gardening service. My properties always look well-maintained.', 4, services[15]),
            ('Robert Williams', 'Homeowner', 'https://i.pravatar.cc/150?img=6',
             'Professional handyman service. Fixed multiple issues in one visit. Great value!', 5, services[18]),
        ]
        
        for idx, (name, designation, image, text, rating, service) in enumerate(testimonials_data):
            Testimonial.objects.get_or_create(
                customer_name=name,
                defaults={
                    'customer_image': image,
                    'customer_designation': designation,
                    'testimonial': text,
                    'rating': rating,
                    'service': service,
                    'is_active': True,
                    'is_featured': idx < 4,
                    'order': idx
                }
            )

    def create_blog_posts(self, admins, categories):
        self.stdout.write('Creating blog posts...')
        
        posts = [
            ('Top 10 Home Cleaning Tips', 'home-cleaning-tips',
             'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=1200&h=800&fit=crop',
             'Discover the best cleaning tips from professionals', categories[0]),
            ('How to Prepare for a House Move', 'prepare-house-move',
             'https://images.unsplash.com/photo-1600518464441-9154a4dea21b?w=1200&h=800&fit=crop',
             'Essential checklist for a stress-free move', categories[1]),
            ('Common Plumbing Problems and Solutions', 'plumbing-problems-solutions',
             'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?w=1200&h=800&fit=crop',
             'Learn how to identify and fix common plumbing issues', categories[2]),
        ]
        
        for title, slug, image, excerpt, category in posts:
            BlogPost.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'featured_image': image,
                    'excerpt': excerpt,
                    'content': f'<p>{excerpt}</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit...</p>',
                    'author': random.choice(admins),
                    'category': category,
                    'is_published': True,
                    'is_featured': True,
                    'published_at': timezone.now() - timedelta(days=random.randint(1, 30)),
                    'views_count': random.randint(100, 1000)
                }
            )

    def create_service_requests(self, customers, services):
        self.stdout.write('Creating service requests...')
        
        for i in range(10):
            customer = random.choice(customers)
            service = random.choice(services)
            
            ServiceRequest.objects.get_or_create(
                email=customer.email,
                service=service,
                defaults={
                    'user': customer,
                    'first_name': customer.first_name,
                    'last_name': customer.last_name,
                    'phone': customer.phone,
                    'pricing_tier': random.choice(['basic', 'standard', 'premium']),
                    'booking_estimate': random.choice(['2-3 Hrs', '4-6 Hrs', '1 Day']),
                    'booking_datetime': timezone.now() + timedelta(days=random.randint(1, 30)),
                    'number_of_people': random.randint(1, 3),
                    'collection_address': f'{random.randint(1, 200)} Main Street',
                    'collection_postal_code': f'E{random.randint(1, 20)} {random.randint(1, 9)}XX',
                    'collection_city': 'London',
                    'collection_property_type': random.choice(['house', 'flat', 'business']),
                    'collection_bedrooms': random.randint(1, 4),
                    'cc_zone': random.choice([True, False]),
                    'status': random.choice(['pending', 'contacted', 'quoted']),
                }
            )
