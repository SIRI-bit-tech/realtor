from django.contrib import admin
from .models import PageView, PropertyView, SearchQuery, UserActivity

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'url')
    search_fields = ('url', 'user__username', 'ip_address')
    date_hierarchy = 'timestamp'

@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'property__property_type')
    search_fields = ('property__title', 'user__username', 'ip_address')
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('property', 'user')

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'results_count', 'user', 'timestamp')
    list_filter = ('timestamp', 'results_count')
    search_fields = ('query', 'user__username')
    date_hierarchy = 'timestamp'

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'property', 'timestamp')
    list_filter = ('timestamp', 'action')
    search_fields = ('user__username', 'action', 'property__title')
    date_hierarchy = 'timestamp'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'property')
