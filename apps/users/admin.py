from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = [
        'preferred_contact', 'budget_min', 'budget_max',
        'preferred_locations', 'property_preferences', 'saved_searches'
    ]

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'user_type', 'is_verified', 'is_active', 'date_joined',
        'avatar_preview'
    ]
    list_filter = [
        'user_type', 'is_verified', 'is_active', 'is_staff',
        'date_joined', 'last_login'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['date_joined', 'last_login', 'avatar_preview']
    list_editable = ['is_verified']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Information', {
            'fields': (
                'user_type', 'phone', 'avatar', 'avatar_preview',
                'bio', 'location', 'website', 'is_verified'
            )
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('user_type', 'phone', 'email')
        }),
    )

    inlines = [UserProfileInline]

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />',
                obj.avatar.url
            )
        return "No avatar"
    avatar_preview.short_description = 'Avatar'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'preferred_contact', 'budget_range',
        'location_count', 'search_count'
    ]
    list_filter = ['preferred_contact']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user']

    def budget_range(self, obj):
        if obj.budget_min and obj.budget_max:
            return f"${obj.budget_min:,.0f} - ${obj.budget_max:,.0f}"
        elif obj.budget_min:
            return f"${obj.budget_min:,.0f}+"
        elif obj.budget_max:
            return f"Up to ${obj.budget_max:,.0f}"
        return "Not set"
    budget_range.short_description = 'Budget Range'

    def location_count(self, obj):
        return len(obj.preferred_locations) if obj.preferred_locations else 0
    location_count.short_description = 'Preferred Locations'

    def search_count(self, obj):
        return len(obj.saved_searches) if obj.saved_searches else 0
    search_count.short_description = 'Saved Searches'
