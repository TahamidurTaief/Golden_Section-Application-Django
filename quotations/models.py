from django.db import models
from django.utils import timezone
from accounts.models import User
from services.models import Service


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
        help_text='e.g., "2-3 Hrs", "1 Day"'
    )
    booking_datetime = models.DateTimeField(help_text='Preferred date and time')
    number_of_people = models.IntegerField(default=1)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Collection Address
    collection_address = models.TextField()
    collection_postal_code = models.CharField(max_length=20)
    collection_city = models.CharField(max_length=100)
    collection_property_type = models.CharField(
        max_length=50, 
        choices=PROPERTY_TYPE_CHOICES,
        default='house'
    )
    collection_bedrooms = models.IntegerField(default=0)
    collection_floor_level = models.CharField(max_length=50, blank=True)
    collection_has_lift = models.BooleanField(default=False)
    
    # Delivery Address
    delivery_address = models.TextField(blank=True)
    delivery_postal_code = models.CharField(max_length=20, blank=True)
    delivery_city = models.CharField(max_length=100, blank=True)
    delivery_property_type = models.CharField(
        max_length=50, 
        choices=PROPERTY_TYPE_CHOICES,
        blank=True
    )
    delivery_bedrooms = models.IntegerField(default=0)
    delivery_floor_level = models.CharField(max_length=50, blank=True)
    delivery_has_lift = models.BooleanField(default=False)
    
    # Additional Information
    additional_notes = models.TextField(blank=True)
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
    admin_notes = models.TextField(blank=True)
    
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
        # Calculate total amount
        cc_charge = 15.00 if self.cc_zone else 0.00
        self.cc_zone_charge = cc_charge
        
        subtotal = self.booking_charges + cc_charge + (self.hourly_rate or 0)
        self.vat = round(subtotal * 0.20, 2)  # 20% VAT
        self.total_amount = subtotal + self.vat
        
        super().save(*args, **kwargs)
    
    @property
    def customer_name(self):
        return f"{self.first_name} {self.last_name}"


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
    breakdown = models.TextField(help_text='Price breakdown details')
    estimated_duration = models.CharField(max_length=100)
    terms_conditions = models.TextField(blank=True)
    
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
