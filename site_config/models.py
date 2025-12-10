from django.db import models
from django.core.validators import URLValidator


class SiteConfiguration(models.Model):
    """Singleton model for site-wide configuration"""
    
    # Basic Info
    site_name = models.CharField(max_length=200, default='Golden Section')
    site_tagline = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(upload_to='site/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site/', null=True, blank=True)
    
    # Contact Info
    primary_email = models.EmailField()
    primary_phone = models.CharField(max_length=20)
    default_whatsapp = models.CharField(
        max_length=20, 
        help_text='Default WhatsApp number with country code (e.g., +447123456789)'
    )
    address = models.TextField(blank=True)
    
    # SEO Meta Tags
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Tracking & Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text='GA4 Measurement ID (e.g., G-XXXXXXXXXX)')
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    # Footer Content
    footer_description = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True, default='© 2025 Golden Section. All rights reserved.')
    
    # Business Hours (JSON format)
    business_hours = models.TextField(
        blank=True,
        help_text='Business hours in JSON format: {"Monday": "9:00 AM - 5:00 PM", ...}'
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'site_configuration'
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass
    
    @classmethod
    def load(cls):
        """Load or create the single instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return self.site_name


class ImportantLink(models.Model):
    """Footer important links"""
    
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=500, help_text='URL or path (e.g., /about or https://example.com)')
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(default=False, help_text='Open link in new tab')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'important_links'
        ordering = ['order', 'title']
        verbose_name = 'Important Link'
        verbose_name_plural = 'Important Links'
    
    def __str__(self):
        return self.title
