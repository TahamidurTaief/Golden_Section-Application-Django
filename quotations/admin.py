from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceRequest, RequestAttachment, QuotationResponse


class RequestAttachmentInline(admin.TabularInline):
    model = RequestAttachment
    extra = 0
    readonly_fields = ['file_name', 'file_type', 'file_size', 'uploaded_at']
    fields = ['file', 'file_name', 'file_type', 'uploaded_at']
    can_delete = True


class QuotationResponseInline(admin.StackedInline):
    model = QuotationResponse
    extra = 0
    fields = ['quoted_price', 'breakdown', 'estimated_duration', 'valid_until', 'terms_conditions']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer_name', 'service', 'booking_date', 'booking_time',
        'total_amount', 'status', 'whatsapp_sent', 'created_at'
    ]
    list_filter = ['status', 'whatsapp_sent', 'cc_zone', 'created_at', 'service__category']
    search_fields = [
        'first_name', 'last_name', 'email', 'phone', 
        'service__name', 'location_address'
    ]
    list_editable = ['status']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    inlines = [RequestAttachmentInline, QuotationResponseInline]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Service Details', {
            'fields': ('service', 'pricing_tier', 'booking_estimate', 'number_of_people', 'hourly_rate')
        }),
        ('Booking Schedule', {
            'fields': ('booking_date', 'booking_time', 'booking_datetime')
        }),
        ('Location Details', {
            'fields': ('location_address', 'location_latitude', 'location_longitude')
        }),
        ('Pricing', {
            'fields': ('booking_charges', 'cc_zone', 'cc_zone_charge', 'vat', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('additional_notes', 'admin_notes')
        }),
        ('Status & Communication', {
            'fields': ('status', 'whatsapp_sent', 'whatsapp_sent_at', 'whatsapp_number_used')
        }),
    )
    
    readonly_fields = ['cc_zone_charge', 'vat', 'total_amount', 'whatsapp_sent_at', 'created_at', 'updated_at']
    
    def customer_name(self, obj):
        return obj.customer_name
    customer_name.short_description = 'Customer'
    
    actions = ['mark_as_contacted', 'mark_as_quoted', 'send_to_whatsapp']
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(status='contacted')
        self.message_user(request, f'{updated} requests marked as contacted.')
    mark_as_contacted.short_description = 'Mark as Contacted'
    
    def mark_as_quoted(self, request, queryset):
        updated = queryset.update(status='quoted')
        self.message_user(request, f'{updated} requests marked as quoted.')
    mark_as_quoted.short_description = 'Mark as Quoted'
    
    def send_to_whatsapp(self, request, queryset):
        # This would integrate with WhatsApp API
        self.message_user(request, 'WhatsApp integration pending.')
    send_to_whatsapp.short_description = 'Send to WhatsApp'


@admin.register(RequestAttachment)
class RequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ['request', 'file_name', 'file_type', 'file_size', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['request__first_name', 'request__last_name', 'file_name']
    ordering = ['-uploaded_at']


@admin.register(QuotationResponse)
class QuotationResponseAdmin(admin.ModelAdmin):
    list_display = ['request', 'quoted_price', 'estimated_duration', 'valid_until', 'sent_at']
    list_filter = ['sent_at', 'valid_until']
    search_fields = ['request__first_name', 'request__last_name', 'breakdown']
    ordering = ['-sent_at']
    readonly_fields = ['sent_at']
