from django.contrib import admin
from .models import Provider, ProviderGallery, ProviderReview


class ProviderGalleryInline(admin.TabularInline):
    model = ProviderGallery
    extra = 1
    fields = ['image', 'caption', 'order']


class ProviderReviewInline(admin.TabularInline):
    model = ProviderReview
    extra = 0
    readonly_fields = ['user', 'service', 'rating', 'title', 'comment', 'created_at']
    fields = ['user', 'rating', 'title', 'is_approved', 'is_featured']
    can_delete = False


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = [
        'business_name', 'user', 'email', 'phone', 'rating', 
        'is_verified', 'is_featured', 'is_active', 'created_at'
    ]
    list_filter = ['is_verified', 'is_featured', 'is_active', 'is_available', 'created_at']
    search_fields = ['business_name', 'user__username', 'email', 'phone', 'city']
    list_editable = ['is_verified', 'is_featured', 'is_active']
    ordering = ['-is_featured', '-rating', '-created_at']
    inlines = [ProviderGalleryInline, ProviderReviewInline]
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Business Information', {
            'fields': ('business_name', 'business_logo', 'bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'website')
        }),
        ('Location', {
            'fields': ('address', 'city', 'postal_code', 'latitude', 'longitude')
        }),
        ('Services & Categories', {
            'fields': ('services', 'categories'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_documents', 'verified_at')
        }),
        ('Statistics', {
            'fields': ('rating', 'total_reviews', 'total_jobs', 'total_completed_jobs'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_available')
        }),
    )
    
    readonly_fields = ['rating', 'total_reviews', 'total_jobs', 'total_completed_jobs']
    filter_horizontal = ['services', 'categories']


@admin.register(ProviderGallery)
class ProviderGalleryAdmin(admin.ModelAdmin):
    list_display = ['provider', 'caption', 'order', 'created_at']
    list_filter = ['provider', 'created_at']
    search_fields = ['provider__business_name', 'caption']
    ordering = ['provider', 'order']


@admin.register(ProviderReview)
class ProviderReviewAdmin(admin.ModelAdmin):
    list_display = ['provider', 'user', 'service', 'rating', 'is_approved', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['provider__business_name', 'user__username', 'title', 'comment']
    list_editable = ['is_approved', 'is_featured']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
