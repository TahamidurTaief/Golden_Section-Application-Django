from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Service categories"""
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True,
        help_text='Category-specific WhatsApp number. Leave empty to use default.'
    )
    
    # Display settings
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'categories'
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_whatsapp(self):
        """Returns category WhatsApp or default from site config"""
        if self.whatsapp_number:
            return self.whatsapp_number
        from site_config.models import SiteConfiguration
        return SiteConfiguration.load().default_whatsapp
    
    @property
    def total_services(self):
        return self.services.filter(is_active=True).count()


class SubCategory(models.Model):
    """Service subcategories"""
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='subcategories'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='subcategories/icons/', null=True, blank=True)
    image = models.ImageField(upload_to='subcategories/', null=True, blank=True)
    
    # Display settings
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order (lower numbers first)')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subcategories'
        ordering = ['category', 'order', 'name']
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
        unique_together = ['category', 'slug']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def total_services(self):
        return self.services.filter(is_active=True).count()
