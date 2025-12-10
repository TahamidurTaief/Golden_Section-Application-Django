from django.contrib import admin
from .models import Service, ServicePricingTier, ServiceGallery


class ServicePricingTierInline(admin.TabularInline):
    model = ServicePricingTier
    extra = 1
    fields = ['tier_type', 'name', 'price', 'description', 'is_active', 'is_recommended', 'order']


class ServiceGalleryInline(admin.TabularInline):
    model = ServiceGallery
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'subcategory', 'is_featured', 
        'is_popular', 'is_active', 'rating', 'views_count', 'created_at'
    ]
    list_filter = ['category', 'subcategory', 'is_featured', 'is_popular', 'is_active', 'created_at']
    search_fields = ['name', 'short_description', 'description']
    list_editable = ['is_featured', 'is_popular', 'is_active', 'rating']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-is_featured', 'order', '-created_at']
    inlines = [ServicePricingTierInline, ServiceGalleryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'subcategory', 'name', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('featured_image', 'gallery_images')
        }),
        ('Contact', {
            'fields': ('whatsapp_number',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_popular', 'is_active', 'order', 'rating', 'views_count')
        }),
    )
    
    readonly_fields = ['views_count']


@admin.register(ServicePricingTier)
class ServicePricingTierAdmin(admin.ModelAdmin):
    list_display = ['service', 'tier_type', 'name', 'price', 'is_active', 'is_recommended']
    list_filter = ['tier_type', 'is_active', 'is_recommended', 'service__category']
    search_fields = ['service__name', 'name', 'description']
    list_editable = ['is_active', 'is_recommended']
    ordering = ['service', 'order', 'tier_type']


@admin.register(ServiceGallery)
class ServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ['service', 'caption', 'order']
    list_filter = ['service__category']
    search_fields = ['service__name', 'caption']
    ordering = ['service', 'order']
