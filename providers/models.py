from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from accounts.models import User
from services.models import Service
from categories.models import Category
from ckeditor.fields import RichTextField


class Provider(models.Model):
    """Provider profile for service providers"""
    
    # User relationship
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='provider_profile'
    )
    
    # Business Information
    business_name = models.CharField(max_length=300)
    business_logo = ProcessedImageField(
        upload_to='providers/logos/',
        processors=[ResizeToFill(300, 300)],
        format='WEBP',
        options={'quality': 90},
        null=True,
        blank=True,
        help_text='Business logo (optimized automatically)'
    )
    
    # ImageKit specifications for different uses
    logo_thumbnail = ImageSpecField(
        source='business_logo',
        processors=[ResizeToFill(100, 100)],
        format='WEBP',
        options={'quality': 85}
    )
    
    logo_card = ImageSpecField(
        source='business_logo',
        processors=[ResizeToFill(150, 150)],
        format='WEBP',
        options={'quality': 85}
    )
    
    bio = models.TextField(help_text='Tell us about your business')
    
    # Contact Information
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Location
    address = RichTextField(config_name='default')
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text='For map display'
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True,
        help_text='For map display'
    )
    
    # Services & Categories
    services = models.ManyToManyField(Service, related_name='providers', blank=True)
    categories = models.ManyToManyField(Category, related_name='providers', blank=True)
    
    # Verification & Documents
    is_verified = models.BooleanField(default=False, help_text='Admin verified provider')
    verification_documents = models.JSONField(
        default=list, 
        blank=True,
        help_text='List of uploaded document URLs'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Statistics
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(default=0)
    total_jobs = models.IntegerField(default=0)
    total_completed_jobs = models.IntegerField(default=0)
    
    # Status & Display
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show in featured providers')
    is_available = models.BooleanField(default=True, help_text='Currently accepting jobs')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'providers'
        ordering = ['-is_featured', '-rating', '-created_at']
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
    
    def __str__(self):
        return self.business_name
    
    @property
    def success_rate(self):
        """Calculate job success rate"""
        if self.total_jobs > 0:
            return round((self.total_completed_jobs / self.total_jobs) * 100, 2)
        return 0


class ProviderGallery(models.Model):
    """Provider work gallery/portfolio"""
    
    provider = models.ForeignKey(
        Provider, 
        on_delete=models.CASCADE, 
        related_name='gallery'
    )
    image = ProcessedImageField(
        upload_to='providers/gallery/',
        processors=[ResizeToFit(1200, 900)],
        format='WEBP',
        options={'quality': 90},
        help_text='Gallery image (optimized automatically)'
    )
    
    # ImageKit specifications for different uses
    image_gallery = ImageSpecField(
        source='image',
        processors=[ResizeToFit(1200, 900)],
        format='WEBP',
        options={'quality': 95}
    )
    
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(200, 200)],
        format='WEBP',
        options={'quality': 80}
    )
    
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'provider_gallery'
        ordering = ['provider', 'order', '-created_at']
        verbose_name = 'Provider Gallery'
        verbose_name_plural = 'Provider Gallery'
    
    def __str__(self):
        return f"{self.provider.business_name} - {self.caption or 'Image'}"


class ProviderReview(models.Model):
    """Customer reviews for providers"""
    
    provider = models.ForeignKey(
        Provider, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='provider_reviews'
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Status
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'provider_reviews'
        ordering = ['-created_at']
        verbose_name = 'Provider Review'
        verbose_name_plural = 'Provider Reviews'
        unique_together = ['provider', 'user', 'service']
    
    def __str__(self):
        return f"{self.user.username} - {self.provider.business_name} ({self.rating}★)"
