from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Avg, Count
from .models import Agency, Agent, AgentReview


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'phone', 'email', 'agent_count',
        'established_year', 'logo_preview'
    ]
    search_fields = ['name', 'email', 'phone']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['logo_preview']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'logo', 'logo_preview')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'website')
        }),
        ('Business Details', {
            'fields': ('license_number', 'established_year')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',)
        })
    )

    def agent_count(self, obj):
        return obj.agents.count()

    agent_count.short_description = 'Agents'

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px;" />',
                obj.logo.url
            )
        return "No logo"

    logo_preview.short_description = 'Logo Preview'


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'agency', 'license_number', 'years_experience',
        'total_sales', 'average_rating', 'is_active', 'is_featured'
    ]
    list_filter = [
        'is_active', 'is_featured', 'agency', 'years_experience',
        'created_at'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'license_number', 'agency__name'
    ]
    readonly_fields = [
        'total_sales', 'total_volume', 'average_rating',
        'created_at', 'updated_at', 'avatar_preview'
    ]
    list_editable = ['is_active', 'is_featured']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar_preview')
        }),
        ('Professional Details', {
            'fields': ('agency', 'license_number', 'years_experience', 'specializations')
        }),
        ('Contact Information', {
            'fields': ('office_phone', 'mobile_phone', 'fax')
        }),
        ('Professional Background', {
            'fields': ('education', 'certifications', 'awards'),
            'classes': ('collapse',)
        }),
        ('Languages', {
            'fields': ('languages',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('total_sales', 'total_volume', 'average_rating'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def avatar_preview(self, obj):
        if obj.user.avatar:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 50%;" />',
                obj.user.avatar.url
            )
        return "No avatar"

    avatar_preview.short_description = 'Avatar'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'agency'
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )


@admin.register(AgentReview)
class AgentReviewAdmin(admin.ModelAdmin):
    list_display = [
        'agent', 'reviewer', 'rating', 'title',
        'is_verified', 'created_at'
    ]
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = [
        'agent__user__username', 'reviewer__username',
        'title', 'comment'
    ]
    readonly_fields = ['created_at']
    list_editable = ['is_verified']

    fieldsets = (
        ('Review Information', {
            'fields': ('agent', 'reviewer', 'rating', 'title')
        }),
        ('Review Content', {
            'fields': ('comment',)
        }),
        ('Status', {
            'fields': ('is_verified', 'created_at')
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'agent__user', 'reviewer'
        )
