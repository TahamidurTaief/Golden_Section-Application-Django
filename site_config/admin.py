from django.contrib import admin
from .models import SiteConfiguration, ImportantLink


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('primary_email', 'primary_phone', 'default_whatsapp', 'address')
        }),
        ('SEO Meta Tags', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Tracking & Analytics', {
            'fields': ('google_analytics_id', 'facebook_pixel_id'),
            'classes': ('collapse',)
        }),
        ('Footer', {
            'fields': ('footer_description', 'copyright_text', 'business_hours'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only one instance allowed
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False


@admin.register(ImportantLink)
class ImportantLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'order', 'is_active', 'open_new_tab']
    list_filter = ['is_active', 'open_new_tab']
    search_fields = ['title', 'url']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'title']
