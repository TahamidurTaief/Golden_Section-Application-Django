from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
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
    
    # Basic Information
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    
    # Media
    featured_image = models.ImageField(upload_to='services/')
    gallery_images = models.JSONField(
        default=list, 
        blank=True,
        help_text='List of additional image URLs'
    )
    
    # Contact
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Service-specific WhatsApp. Leave empty to use category/default WhatsApp.'
    )
    
    # Status & Display
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')
    is_popular = models.BooleanField(default=False, help_text='Show in popular section')
    is_active = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0.0,
        validators=[MinValueValidator(0)],
        help_text='Service rating (0.0 - 5.0)'
    )
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
    def has_pricing(self):
        return self.pricing_tiers.filter(is_active=True).exists()


class ServicePricingTier(models.Model):
    """Service pricing tiers: Basic, Standard, Premium"""
    
    TIER_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='pricing_tiers'
    )
    tier_type = models.CharField(max_length=20, choices=TIER_CHOICES)
    name = models.CharField(max_length=200, help_text='e.g., "Basic Package"')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text='Price in GBP'
    )
    description = models.TextField()
    features = models.JSONField(
        default=list,
        help_text='List of features included in this tier'
    )
    
    # Display
    is_active = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False, help_text='Highlight as recommended')
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_pricing_tiers'
        unique_together = ['service', 'tier_type']
        ordering = ['service', 'order', 'tier_type']
        verbose_name = 'Service Pricing Tier'
        verbose_name_plural = 'Service Pricing Tiers'
    
    def __str__(self):
        return f"{self.service.name} - {self.get_tier_type_display()}"


class ServiceGallery(models.Model):
    """Additional service images"""
    
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE, 
        related_name='gallery'
    )
    image = models.ImageField(upload_to='services/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'service_gallery'
        ordering = ['service', 'order']
        verbose_name = 'Service Gallery Image'
        verbose_name_plural = 'Service Gallery Images'
    
    def __str__(self):
        return f"{self.service.name} - Image {self.order}"
