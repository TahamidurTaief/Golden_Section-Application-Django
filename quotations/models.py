from django.db import models
from django.utils import timezone
from accounts.models import User
from services.models import Service
from ckeditor.fields import RichTextField


class ServiceRequest(models.Model):
    """Customer service quotation requests"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quoted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PROPERTY_TYPE_CHOICES = [
        ('house', 'House'),
        ('flat', 'Flat/Apartment'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    # User Information
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='service_requests'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Service Details
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE,
        related_name='requests'
    )
    pricing_tier = models.CharField(
        max_length=20, 
        blank=True,
        help_text='basic, standard, or premium'
    )
    
    # Booking Details
    booking_estimate = models.CharField(
        max_length=50, 
        help_text='e.g., "2-3 Hrs", "1 Day"',
        blank=True
    )
    booking_date = models.DateField(help_text='Appointment date', null=True, blank=True)
    booking_time = models.CharField(max_length=20, help_text='Appointment time (e.g., 9:00 AM)', null=True, blank=True)
    booking_datetime = models.DateTimeField(help_text='Combined date and time', null=True, blank=True)
    number_of_people = models.IntegerField(default=1, blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Location Details
    location_address = RichTextField(blank=True, help_text='Full address', config_name='default')
    location_latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True
    )
    location_longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True
    )
    
    # Additional Information
    additional_notes = RichTextField(blank=True, config_name='default')
    cc_zone = models.BooleanField(
        default=False, 
        help_text='Congestion Charge Zone'
    )
    
    # Pricing
    booking_charges = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=42.00
    )
    cc_zone_charge = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    vat = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00
    )
    
    # Status & Communication
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)
    whatsapp_number_used = models.CharField(max_length=20, blank=True)
    
    # Admin Notes
    admin_notes = RichTextField(blank=True, config_name='default')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_requests'
        ordering = ['-created_at']
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service.name} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        # Keep pricing fields for future use but don't auto-calculate
        # Admin can manually set pricing when responding to the request
        if not self.total_amount:
            self.total_amount = 0.00
        
        super().save(*args, **kwargs)
    
    @property
    def customer_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_whatsapp_number(self):
        """Get WhatsApp number for this service request (Service > Category > Default)"""
        if self.service.whatsapp_number:
            return self.service.whatsapp_number
        elif self.service.category.whatsapp_number:
            return self.service.category.whatsapp_number
        else:
            try:
                from site_config.models import SiteConfiguration
                config = SiteConfiguration.load()
                return config.default_whatsapp if config and config.default_whatsapp else None
            except Exception:
                return None


class RequestAttachment(models.Model):
    """File attachments for service requests"""
    
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]
    
    request = models.ForeignKey(
        ServiceRequest, 
        on_delete=models.CASCADE, 
        related_name='attachments'
    )
    file = models.FileField(upload_to='quotations/%Y/%m/')
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES)
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text='File size in bytes')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'request_attachments'
        ordering = ['request', 'uploaded_at']
        verbose_name = 'Request Attachment'
        verbose_name_plural = 'Request Attachments'
    
    def __str__(self):
        return f"{self.request.id} - {self.file_name}"


class QuotationResponse(models.Model):
    """Admin responses to service requests"""
    
    request = models.ForeignKey(
        ServiceRequest, 
        on_delete=models.CASCADE, 
        related_name='quotations'
    )
    
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2)
    breakdown = RichTextField(help_text='Price breakdown details', config_name='default')
    estimated_duration = models.CharField(max_length=100)
    terms_conditions = RichTextField(blank=True, config_name='default')
    
    valid_until = models.DateTimeField(help_text='Quotation valid until')
    
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='sent_quotations'
    )
    
    class Meta:
        db_table = 'quotation_responses'
        ordering = ['-sent_at']
        verbose_name = 'Quotation Response'
        verbose_name_plural = 'Quotation Responses'
    
    def __str__(self):
        return f"Quote for {self.request.id} - £{self.quoted_price}"
