from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from apps.properties.models import Property

User = get_user_model()

class PageView(models.Model):
    """Model to track page views"""
    url = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    query_params = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.url} - {self.timestamp}"

class PropertyView(models.Model):
    """Model to track property views"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='analytics_views')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                            related_name='analytics_property_views')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Property View'
        verbose_name_plural = 'Property Views'
        indexes = [
            models.Index(fields=['property']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.property.title} - {self.timestamp}"

class SearchQuery(models.Model):
    """Model to track search queries"""
    query = models.CharField(max_length=255)
    filters = models.JSONField(default=dict, blank=True)
    results_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Search Query'
        verbose_name_plural = 'Search Queries'
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.query} ({self.results_count} results) - {self.timestamp}"

class UserActivity(models.Model):
    """Model to track user activity"""
    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('register', 'Register'),
        ('favorite', 'Favorite Property'),
        ('unfavorite', 'Unfavorite Property'),
        ('contact_agent', 'Contact Agent'),
        ('save_search', 'Save Search'),
        ('schedule_viewing', 'Schedule Viewing'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
