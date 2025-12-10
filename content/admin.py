from django.contrib import admin
from .models import Page, FAQ, Testimonial, BlogPost, ContactMessage


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type', 'slug', 'is_active', 'show_in_footer', 'updated_at']
    list_filter = ['page_type', 'is_active', 'show_in_footer']
    search_fields = ['title', 'content']
    list_editable = ['is_active', 'show_in_footer']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('page_type', 'title', 'slug', 'content')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'show_in_footer', 'order')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'is_featured', 'order']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'is_featured', 'order']
    ordering = ['order', '-created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'service', 'is_active', 'is_featured', 'order', 'created_at']
    list_filter = ['rating', 'is_active', 'is_featured', 'service']
    search_fields = ['customer_name', 'customer_designation', 'testimonial']
    list_editable = ['is_active', 'is_featured', 'order']
    ordering = ['-is_featured', 'order', '-created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_featured', 'views_count', 'published_at']
    list_filter = ['is_published', 'is_featured', 'category', 'published_at']
    search_fields = ['title', 'excerpt', 'content']
    list_editable = ['is_published', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_at', '-created_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'featured_image', 'excerpt', 'content')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_at')
        }),
    )
    
    readonly_fields = ['views_count']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_replied']
    ordering = ['-created_at']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = 'Mark as Read'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(is_replied=True, is_read=True)
        self.message_user(request, f'{updated} messages marked as replied.')
    mark_as_replied.short_description = 'Mark as Replied'
