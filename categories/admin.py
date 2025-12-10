from django.contrib import admin
from .models import Category, SubCategory


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ['name', 'slug', 'image', 'icon', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'total_services', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'is_featured', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    inlines = [SubCategoryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Media', {
            'fields': ('icon', 'image')
        }),
        ('Contact', {
            'fields': ('whatsapp_number',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
    )


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'total_services', 'is_active', 'order']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['category', 'order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Media', {
            'fields': ('icon', 'image')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
