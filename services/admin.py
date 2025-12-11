from django.contrib import admin
from .models import (
    Service, AdditionalImage, SubService, 
    ServiceInclude, ServiceFAQ, BusinessHours
)


class AdditionalImageInline(admin.TabularInline):
    """Inline for additional service images"""
    model = AdditionalImage
    extra = 1
    fields = ['image', 'caption', 'order']
    ordering = ['order']


class SubServiceInline(admin.TabularInline):
    """Inline for sub-services"""
    model = SubService
    extra = 1
    fields = ['name', 'description', 'icon', 'is_active', 'order']
    ordering = ['order']


class ServiceIncludeInline(admin.TabularInline):
    """Inline for what's included in service"""
    model = ServiceInclude
    extra = 1
    fields = ['title', 'description', 'icon', 'order']
    ordering = ['order']


class ServiceFAQInline(admin.StackedInline):
    """Inline for service FAQs"""
    model = ServiceFAQ
    extra = 1
    fields = ['question', 'answer', 'is_active', 'order']
    ordering = ['order']


class BusinessHoursInline(admin.TabularInline):
    """Inline for business hours"""
    model = BusinessHours
    extra = 7  # All 7 days of the week
    fields = ['weekday', 'opening_time', 'closing_time', 'is_closed']
    ordering = ['weekday']
    
    def get_extra(self, request, obj=None, **kwargs):
        """Only show extra forms if no hours exist yet"""
        if obj and obj.business_hours.exists():
            return 0
        return 7


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'subcategory', 'is_featured', 
        'is_popular', 'is_active', 'rating', 'total_reviews',
        'services_provided', 'views_count', 'created_at'
    ]
    list_filter = ['category', 'subcategory', 'is_featured', 'is_popular', 'is_active', 'created_at']
    search_fields = ['name', 'short_description', 'overview']
    list_editable = ['is_featured', 'is_popular', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-is_featured', 'order', '-created_at']
    inlines = [
        AdditionalImageInline, 
        SubServiceInline, 
        ServiceIncludeInline, 
        ServiceFAQInline, 
        BusinessHoursInline
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'subcategory', 'name', 'slug', 'short_description', 'overview')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Contact', {
            'fields': ('whatsapp_number',)
        }),
        ('Statistics & Metrics', {
            'fields': ('rating', 'total_reviews', 'services_provided', 'views_count'),
            'description': 'Service performance metrics and statistics'
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_popular', 'is_active', 'order')
        }),
    )
    
    readonly_fields = ['views_count']


@admin.register(AdditionalImage)
class AdditionalImageAdmin(admin.ModelAdmin):
    list_display = ['service', 'caption', 'order', 'created_at']
    list_filter = ['service__category', 'created_at']
    search_fields = ['service__name', 'caption']
    ordering = ['service', 'order']


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ['service', 'name', 'is_active', 'order', 'created_at']
    list_filter = ['service__category', 'is_active', 'created_at']
    search_fields = ['service__name', 'name', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['service', 'order']


@admin.register(ServiceInclude)
class ServiceIncludeAdmin(admin.ModelAdmin):
    list_display = ['service', 'title', 'icon', 'order']
    list_filter = ['service__category']
    search_fields = ['service__name', 'title', 'description']
    ordering = ['service', 'order']


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ['service', 'question_preview', 'is_active', 'order', 'created_at']
    list_filter = ['service__category', 'is_active', 'created_at']
    search_fields = ['service__name', 'question', 'answer']
    list_editable = ['is_active', 'order']
    ordering = ['service', 'order']
    
    def question_preview(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ['service', 'weekday_name', 'formatted_hours', 'is_closed']
    list_filter = ['service__category', 'weekday', 'is_closed']
    search_fields = ['service__name']
    ordering = ['service', 'weekday']
    
    def weekday_name(self, obj):
        return obj.get_weekday_display()
    weekday_name.short_description = 'Day'
    
    def formatted_hours(self, obj):
        return obj.formatted_hours
    formatted_hours.short_description = 'Hours'
