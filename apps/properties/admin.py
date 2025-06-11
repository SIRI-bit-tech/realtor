from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    PropertyType, Location, Property, PropertyImage, 
    PropertyFavorite, PropertyView
)

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'property_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def property_count(self, obj):
        return obj.property_set.count()
    property_count.short_description = 'Properties'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'country', 'property_count', 'coordinates']
    list_filter = ['state', 'country']
    search_fields = ['name', 'state']
    prepopulated_fields = {'slug': ('name',)}
    
    def property_count(self, obj):
        return obj.property_set.count()
    property_count.short_description = 'Properties'
    
    def coordinates(self, obj):
        if obj.latitude and obj.longitude:
            return f"{obj.latitude}, {obj.longitude}"
        return "Not set"
    coordinates.short_description = 'Coordinates'

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'property_type', 'listing_type', 'status', 
        'price', 'location', 'agent', 'view_count', 'favorite_count',
        'created_at'
    ]
    list_filter = [
        'status', 'listing_type', 'property_type', 'location__state',
        'created_at', 'bedrooms', 'bathrooms'
    ]
    search_fields = ['title', 'address', 'description', 'mls_number']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'id', 'view_count', 'favorite_count', 'price_per_sqft',
        'created_at', 'updated_at', 'listed_date', 'image_preview'
    ]
    inlines = [PropertyImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'property_type', 
                      'listing_type', 'status', 'agent')
        }),
        ('Location', {
            'fields': ('location', 'address', 'latitude', 'longitude')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'square_feet', 'lot_size',
                      'year_built', 'garage_spaces')
        }),
        ('Pricing', {
            'fields': ('price', 'price_per_sqft', 'hoa_fee', 'property_tax')
        }),
        ('Features', {
            'fields': ('features', 'amenities'),
            'classes': ('collapse',)
        }),
        ('Listing Information', {
            'fields': ('mls_number', 'days_on_market')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'favorite_count', 'created_at', 'updated_at', 'listed_date'),
            'classes': ('collapse',)
        }),
        ('System', {
            'fields': ('id',),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                primary_image.image.url
            )
        return "No primary image"
    image_preview.short_description = 'Primary Image'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'property_type', 'location', 'agent'
        ).prefetch_related('images')

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'alt_text', 'is_primary', 'order', 'image_preview']
    list_filter = ['is_primary', 'property__property_type']
    search_fields = ['property__title', 'alt_text']
    list_editable = ['is_primary', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'

@admin.register(PropertyFavorite)
class PropertyFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']
    list_filter = ['created_at', 'property__property_type']
    search_fields = ['user__username', 'property__title']
    readonly_fields = ['created_at']

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at', 'property__property_type']
    search_fields = ['property__title', 'user__username', 'ip_address']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
