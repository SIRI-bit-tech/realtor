from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from PIL import Image


class User(AbstractUser):
    USER_TYPES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('agent', 'Agent'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='buyer')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_contact = models.CharField(
        max_length=10,
        choices=[('email', 'Email'), ('phone', 'Phone'), ('both', 'Both')],
        default='email'
    )
    budget_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    preferred_locations = models.JSONField(default=list, blank=True)
    property_preferences = models.JSONField(default=dict, blank=True)
    saved_searches = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100, blank=True)
    criteria = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    alert_enabled = models.BooleanField(default=True)
    last_alert_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name or 'Saved Search'}"

    def get_absolute_url(self):
        return reverse('users:saved_search_detail', kwargs={'pk': self.pk})


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("info", "Info"),
        ("success", "Success"),
        ("warning", "Warning"),
        ("error", "Error"),
        ("alert", "Alert"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default="info")
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    broadcast = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_notifications")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username if self.user else 'Broadcast'}: {self.message[:40]}"


class BroadcastRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="read_broadcasts")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="read_by")
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "notification")
        verbose_name = "Broadcast Read Receipt"
        verbose_name_plural = "Broadcast Read Receipts"

    def __str__(self):
        return f"{self.user.username} read {self.notification.id}"
