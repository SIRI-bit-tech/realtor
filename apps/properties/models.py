from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

User = get_user_model()

class PropertyType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # For CSS icon classes
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Property Types"

class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='USA')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}, {self.state}"
    
    class Meta:
        unique_together = ['name', 'state']

class Property(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('off_market', 'Off Market'),
    ]
    
    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    
    # Location
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Property Details
    bedrooms = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)])
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(20)])
    square_feet = models.PositiveIntegerField()
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_built = models.PositiveIntegerField(null=True, blank=True)
    garage_spaces = models.PositiveIntegerField(default=0)
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    hoa_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    property_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Features
    features = models.JSONField(default=list, blank=True)
    amenities = models.JSONField(default=list, blank=True)
    
    # Listing Information
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    mls_number = models.CharField(max_length=50, blank=True)
    days_on_market = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    listed_date = models.DateTimeField(auto_now_add=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'listing_type']),
            models.Index(fields=['location', 'property_type']),
            models.Index(fields=['price']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('properties:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if self.square_feet and self.price:
            self.price_per_sqft = self.price / self.square_feet
        super().save(*args, **kwargs)

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"Image for {self.property.title}"

class PropertyFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'property']

class PropertyView(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                            related_name='property_views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['property', '-created_at']),
        ]

class PropertyReview(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['property', 'reviewer']
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.property.title} by {self.reviewer.username}"
