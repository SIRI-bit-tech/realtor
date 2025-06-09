from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Agency(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='agencies/', blank=True, null=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    license_number = models.CharField(max_length=50, blank=True)
    established_year = models.PositiveIntegerField(null=True, blank=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Agencies"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('agents:agency_detail', kwargs={'slug': self.slug})


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agents')
    license_number = models.CharField(max_length=50)
    specializations = models.JSONField(default=list, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    languages = models.JSONField(default=list, blank=True)

    # Contact Information
    office_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)

    # Professional Details
    education = models.TextField(blank=True)
    certifications = models.JSONField(default=list, blank=True)
    awards = models.JSONField(default=list, blank=True)

    # Statistics
    total_sales = models.PositiveIntegerField(default=0)
    total_volume = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    # Availability
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.agency.name}"

    def get_absolute_url(self):
        return reverse('agents:agent_detail', kwargs={'username': self.user.username})


class AgentReview(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['agent', 'reviewer']
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.agent.user.get_full_name()} by {self.reviewer.username}"
