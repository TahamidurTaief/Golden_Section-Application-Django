from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from ckeditor.fields import RichTextField


class Page(models.Model):
    """Static content pages"""
    
    PAGE_TYPE_CHOICES = [
        ('about', 'About Us'),
        ('terms', 'Terms & Conditions'),
        ('privacy', 'Privacy Policy'),
        ('faq', 'FAQ'),
        ('contact', 'Contact Us'),
        ('custom', 'Custom Page'),
    ]
    
    page_type = models.CharField(
        max_length=50, 
        choices=PAGE_TYPE_CHOICES,
        unique=True
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    content = RichTextField(help_text='HTML content allowed', config_name='awesome_ckeditor')
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = RichTextField(blank=True, config_name='default')
    meta_keywords = RichTextField(blank=True, config_name='default')
    
    # Display
    is_active = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pages'
        ordering = ['order', 'title']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)


class FAQ(models.Model):
    """Frequently Asked Questions"""
    
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='faqs',
        help_text='Optional: Associate with a category'
    )
    
    # Display
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'faqs'
        ordering = ['order', '-created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question[:100]


class Testimonial(models.Model):
    """Customer testimonials"""
    
    customer_name = models.CharField(max_length=200)
    customer_image = ProcessedImageField(
        upload_to='testimonials/',
        processors=[ResizeToFill(200, 200)],
        format='WEBP',
        options={'quality': 90},
        null=True,
        blank=True,
        help_text='Customer photo (optimized automatically)'
    )
    
    image_thumbnail = ImageSpecField(
        source='customer_image',
        processors=[ResizeToFill(100, 100)],
        format='WEBP',
        options={'quality': 85}
    )
    
    customer_designation = models.CharField(max_length=200, blank=True, help_text='e.g., "CEO, Company Name"')
    
    testimonial = models.TextField()
    rating = models.IntegerField(
        default=5,
        choices=[(i, i) for i in range(1, 6)],
        help_text='Rating from 1 to 5'
    )
    
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials'
    )
    
    # Display
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    order = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'testimonials'
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"


class BlogPost(models.Model):
    """Blog posts"""
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    featured_image = ProcessedImageField(
        upload_to='blog/',
        processors=[ResizeToFit(1200, 800)],
        format='WEBP',
        options={'quality': 90},
        help_text='Blog featured image (optimized automatically)'
    )
    
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
    
    excerpt = models.CharField(max_length=500)
    content = models.TextField()
    
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts'
    )
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.TextField(blank=True)
    
    # Display
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    
    # Dates
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'blog_posts'
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Contact form submissions"""
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    
    # Status
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contact_messages'
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
