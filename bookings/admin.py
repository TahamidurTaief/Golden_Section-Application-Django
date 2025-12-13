from django.contrib import admin
from django.utils.html import format_html
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference',
        'customer_name_display',
        'service_display',
        'appointment_display',
        'status_badge',
        'whatsapp_status',
        'created_at'
    ]
    list_filter = [
        'status',
        'whatsapp_sent',
        'appointment_date',
        'service__category',
        'created_at'
    ]
    search_fields = [
        'booking_reference',
        'customer_first_name',
        'customer_last_name',
        'customer_email',
        'customer_phone',
        'service__name'
    ]
    readonly_fields = [
        'booking_reference',
        'created_at',
        'updated_at',
        'whatsapp_sent_at',
        'whatsapp_number_used',
        'google_maps_display'
    ]
    
    fieldsets = (
        ('Booking Information', {
            'fields': (
                'booking_reference',
                'status',
                'service',
                'provider',
                'sub_services'
            )
        }),
        ('Customer Information', {
            'fields': (
                'customer_first_name',
                'customer_last_name',
                'customer_email',
                'customer_phone'
            )
        }),
        ('Appointment Details', {
            'fields': (
                'appointment_date',
                'appointment_time'
            )
        }),
        ('Location', {
            'fields': (
                'location_address',
                'location_latitude',
                'location_longitude',
                'google_maps_display'
            )
        }),
        ('Notes', {
            'fields': (
                'notes',
                'admin_notes'
            ),
            'classes': ('collapse',)
        }),
        ('WhatsApp Notification', {
            'fields': (
                'whatsapp_sent',
                'whatsapp_sent_at',
                'whatsapp_number_used'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['sub_services']
    
    def customer_name_display(self, obj):
        """Display customer full name"""
        return obj.customer_full_name
    customer_name_display.short_description = 'Customer'
    
    def service_display(self, obj):
        """Display service name with category"""
        return format_html(
            '<span style="color: #666;">{}</span><br/><strong>{}</strong>',
            obj.service.category.name,
            obj.service.name
        )
    service_display.short_description = 'Service'
    
    def appointment_display(self, obj):
        """Display appointment date and time"""
        return format_html(
            '<strong>{}</strong><br/><span style="color: #666;">{}</span>',
            obj.appointment_date.strftime('%b %d, %Y'),
            obj.appointment_time
        )
    appointment_display.short_description = 'Appointment'
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'pending': '#FFA500',
            'confirmed': '#4CAF50',
            'in_progress': '#2196F3',
            'completed': '#9C27B0',
            'cancelled': '#F44336'
        }
        color = colors.get(obj.status, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def whatsapp_status(self, obj):
        """Display WhatsApp sent status"""
        if obj.whatsapp_sent:
            return format_html(
                '<span style="color: #25D366;">✓ Sent</span>'
            )
        return format_html(
            '<span style="color: #999;">✗ Not Sent</span>'
        )
    whatsapp_status.short_description = 'WhatsApp'
    
    def google_maps_display(self, obj):
        """Display Google Maps link"""
        if obj.location_latitude and obj.location_longitude:
            return format_html(
                '<a href="{}" target="_blank" style="color: #4285F4;">📍 View on Google Maps</a>',
                obj.google_maps_link
            )
        return '-'
    google_maps_display.short_description = 'Map Location'
    
    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled', 'resend_whatsapp']
    
    def mark_as_confirmed(self, request, queryset):
        """Mark selected bookings as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} booking(s) marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark as Confirmed'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected bookings as completed"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_as_completed.short_description = 'Mark as Completed'
    
    def mark_as_cancelled(self, request, queryset):
        """Mark selected bookings as cancelled"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_as_cancelled.short_description = 'Mark as Cancelled'
    
    def resend_whatsapp(self, request, queryset):
        """Resend WhatsApp notification for selected bookings"""
        from .utils import send_whatsapp_notification
        sent_count = 0
        for booking in queryset:
            if send_whatsapp_notification(booking):
                sent_count += 1
        self.message_user(request, f'WhatsApp notification sent for {sent_count} booking(s).')
    resend_whatsapp.short_description = 'Resend WhatsApp Notification'
