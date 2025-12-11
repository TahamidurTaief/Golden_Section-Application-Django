from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from categories.models import Category, SubCategory


class Service(models.Model):
    """Main service model"""
    
    # Relationships
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='services'
    )
    subcategory = models.ForeignKey(
        SubCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='services'
    )
    provider = models.ForeignKey(
        'providers.Provider',
        on_delete=models.CASCADE,
        related_name='services_provided',
        null=True,
        blank=True,
        help_text='Service provider'
    )
    
    # Basic Information
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    short_description = models.CharField(max_length=500)
    overview = models.TextField(default='', help_text='Detailed overview of the service')
    
    # Media
    featured_image = ProcessedImageField(
        upload_to='services/',
        processors=[ResizeToFit(1200, 800)],
        format='WEBP',
        options={'quality': 90},
        help_text='Main service image (optimized automatically)'
    )
    
    # ImageKit specifications for different uses
    image_card = ImageSpecField(
        source='featured_image',
        processors=[ResizeToFill(400, 300)],
        format='WEBP',
        options={'quality': 85}
    )
    
    image_detail = ImageSpecField(
        source='featured_image',
        processors=[ResizeToFit(800, 600)],
        format='WEBP',
        options={'quality': 90}
    )
    
    image_gallery = ImageSpecField(
        source='featured_image',
        processors=[ResizeToFit(1200, 900)],
        format='WEBP',
        options={'quality': 95}
    )
    
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for featured image (for accessibility)'
    )
    
    # Contact
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Service-specific WhatsApp. Leave empty to use category/default WhatsApp.'
    )
    
    # Statistics & Metrics
    views_count = models.IntegerField(default=0, help_text='Number of times viewed')
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0)],
        help_text='Average service rating (0.0 - 5.0)'
    )
    total_reviews = models.IntegerField(default=0, help_text='Total number of reviews')
    services_provided = models.IntegerField(default=0, help_text='Total services completed')
    
    # Status & Display
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')
    is_popular = models.BooleanField(default=False, help_text='Show in popular section')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'services'
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_whatsapp(self):
        """Priority: Service > Category > Default"""
        if self.whatsapp_number:
            return self.whatsapp_number
        return self.category.get_whatsapp()
    
    @property
    def average_rating_display(self):
        """Return formatted rating"""
        return f"{self.rating:.1f}"
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class AdditionalImage(models.Model):
    """Additional images for services"""
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='additional_images'
    )
    image = ProcessedImageField(
        upload_to='services/additional/',
        processors=[ResizeToFit(1200, 900)],
        format='WEBP',
        options={'quality': 90},
        help_text='Additional service image (optimized automatically)'
    )
    
    # ImageKit specification for gallery display
    image_gallery = ImageSpecField(
        source='image',
        processors=[ResizeToFit(1200, 900)],
        format='WEBP',
        options={'quality': 95}
    )
    
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(150, 150)],
        format='WEBP',
        options={'quality': 80}
    )
    
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for image (for accessibility)'
    )
    order = models.IntegerField(default=0, help_text='Display order')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'service_additional_images'
        ordering = ['service', 'order']
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'
    
    def __str__(self):
        return f"{self.service.name} - Image {self.order}"


class SubService(models.Model):
    """Sub-services under main service (e.g., Fan, AC, Light maintenance under Electrical)"""
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='sub_services'
    )
    name = models.CharField(max_length=200, help_text='e.g., Fan Repair, AC Installation')
    description = models.TextField(blank=True)
    image = ProcessedImageField(
        upload_to='services/sub_services/',
        processors=[ResizeToFill(200, 200)],
        format='WEBP',
        options={'quality': 85},
        null=True,
        blank=True,
        help_text='Sub-service image (optimized automatically)'
    )
    
    # ImageKit specification for thumbnail display
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='WEBP',
        options={'quality': 80}
    )
    
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text='Alt text for image (for accessibility)'
    )
    icon = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Icon class (e.g., feather-fan, ti-air-conditioning)'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='Price for this sub-service'
    )
    duration = models.IntegerField(
        default=30,
        help_text='Duration in minutes'
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_sub_services'
        ordering = ['service', 'order', 'name']
        verbose_name = 'Sub Service'
        verbose_name_plural = 'Sub Services'
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ServiceInclude(models.Model):
    """What's included in the service"""
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='includes'
    )
    title = models.CharField(max_length=200, help_text='e.g., Free Consultation, 24/7 Support')
    description = models.TextField(blank=True, help_text='Optional detailed description')
    icon = models.CharField(
        max_length=50, 
        blank=True,
        help_text='Icon class (e.g., feather-check, ti-shield-check)'
    )
    order = models.IntegerField(default=0, help_text='Display order')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'service_includes'
        ordering = ['service', 'order']
        verbose_name = 'Service Include'
        verbose_name_plural = 'Service Includes'
    
    def __str__(self):
        return f"{self.service.name} - {self.title}"


class ServiceFAQ(models.Model):
    """Frequently Asked Questions for services"""
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='faqs'
    )
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0, help_text='Display order')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_faqs'
        ordering = ['service', 'order']
        verbose_name = 'Service FAQ'
        verbose_name_plural = 'Service FAQs'
    
    def __str__(self):
        return f"{self.service.name} - {self.question[:50]}"


class BusinessHours(models.Model):
    """Business hours for services"""
    
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='business_hours'
    )
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        help_text='Day of the week'
    )
    opening_time = models.TimeField(null=True, blank=True, help_text='Opening time (e.g., 09:30 AM)')
    closing_time = models.TimeField(null=True, blank=True, help_text='Closing time (e.g., 07:00 PM)')
    is_closed = models.BooleanField(default=False, help_text='Check if closed on this day')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_business_hours'
        unique_together = ['service', 'weekday']
        ordering = ['service', 'weekday']
        verbose_name = 'Business Hours'
        verbose_name_plural = 'Business Hours'
    
    def __str__(self):
        weekday_name = self.get_weekday_display()
        if self.is_closed:
            return f"{self.service.name} - {weekday_name}: Closed"
        return f"{self.service.name} - {weekday_name}: {self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"
    
    @property
    def formatted_hours(self):
        """Return formatted business hours"""
        if self.is_closed:
            return "Closed"
        return f"{self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"
