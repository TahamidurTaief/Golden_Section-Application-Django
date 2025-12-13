from django.db import models
from django.core.validators import RegexValidator
from services.models import Service, SubService
from providers.models import Provider
from ckeditor.fields import RichTextField


class Booking(models.Model):
    """Booking/Appointment model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Service Information
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text='Main service booked'
    )
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text='Service provider',
        null=True,
        blank=True
    )
    sub_services = models.ManyToManyField(
        SubService,
        related_name='bookings',
        blank=True,
        help_text='Selected sub-services'
    )
    
    # Customer Information
    customer_first_name = models.CharField(max_length=100, help_text='Customer first name')
    customer_last_name = models.CharField(max_length=100, help_text='Customer last name')
    customer_email = models.EmailField(help_text='Customer email address')
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+971501234567'. Up to 15 digits allowed."
    )
    customer_phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        help_text='Customer phone number'
    )
    
    # Location Information
    location_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text='Service location latitude'
    )
    location_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text='Service location longitude'
    )
    location_address = RichTextField(help_text='Full service location address', config_name='default')
    
    # Appointment Information
    appointment_date = models.DateField(help_text='Scheduled appointment date')
    appointment_time = models.CharField(max_length=20, help_text='Scheduled appointment time (e.g., 10:00 AM)')
    
    # Status and Notes
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Booking status'
    )
    notes = RichTextField(blank=True, help_text='Additional notes or special instructions', config_name='default')
    admin_notes = RichTextField(blank=True, help_text='Internal admin notes', config_name='default')
    
    # WhatsApp Message
    whatsapp_sent = models.BooleanField(default=False, help_text='WhatsApp notification sent')
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True, help_text='WhatsApp sent timestamp')
    whatsapp_number_used = models.CharField(
        max_length=20,
        blank=True,
        help_text='WhatsApp number used for notification'
    )
    
    # Metadata
    booking_reference = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text='Unique booking reference number'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.booking_reference} - {self.customer_full_name} - {self.service.name}"
    
    def save(self, *args, **kwargs):
        # Generate booking reference if not exists
        if not self.booking_reference:
            import uuid
            from datetime import datetime
            # Format: BK-YYYYMMDD-XXXX (e.g., BK-20251211-A1B2)
            date_str = datetime.now().strftime('%Y%m%d')
            unique_id = uuid.uuid4().hex[:4].upper()
            self.booking_reference = f"BK-{date_str}-{unique_id}"
        
        super().save(*args, **kwargs)
    
    @property
    def customer_full_name(self):
        """Return full customer name"""
        return f"{self.customer_first_name} {self.customer_last_name}"
    
    @property
    def formatted_appointment_datetime(self):
        """Return formatted appointment date and time"""
        from datetime import datetime
        
        # Handle both date objects and string dates
        if isinstance(self.appointment_date, str):
            try:
                date_obj = datetime.strptime(self.appointment_date, '%Y-%m-%d').date()
                formatted_date = date_obj.strftime('%B %d, %Y')
            except (ValueError, AttributeError):
                formatted_date = self.appointment_date
        else:
            formatted_date = self.appointment_date.strftime('%B %d, %Y')
        
        return f"{formatted_date} at {self.appointment_time}"
    
    @property
    def sub_services_list(self):
        """Return list of sub-service names"""
        return ", ".join([sub.name for sub in self.sub_services.all()])
    
    @property
    def google_maps_link(self):
        """Generate Google Maps link from coordinates"""
        return f"https://www.google.com/maps?q={self.location_latitude},{self.location_longitude}"
    
    def get_whatsapp_number(self):
        """Get WhatsApp number for this booking (Service > Category > Default)"""
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
