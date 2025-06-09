import django_filters
from django import forms
from django.db.models import Q
from .models import Property, PropertyType, Location


class PropertyFilter(django_filters.FilterSet):
    listing_type = django_filters.ChoiceFilter(
        choices=Property.LISTING_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    property_type = django_filters.ModelChoiceFilter(
        queryset=PropertyType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    price_min = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price'
        })
    )

    price_max = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price'
        })
    )

    bedrooms = django_filters.NumberFilter(
        field_name='bedrooms',
        lookup_expr='gte',
        widget=forms.Select(
            choices=[(i, f'{i}+') for i in range(1, 6)],
            attrs={'class': 'form-select'}
        )
    )

    bathrooms = django_filters.NumberFilter(
        field_name='bathrooms',
        lookup_expr='gte',
        widget=forms.Select(
            choices=[(i, f'{i}+') for i in range(1, 6)],
            attrs={'class': 'form-select'}
        )
    )

    square_feet_min = django_filters.NumberFilter(
        field_name='square_feet',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Sq Ft'
        })
    )

    square_feet_max = django_filters.NumberFilter(
        field_name='square_feet',
        lookup_expr='lte',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Sq Ft'
        })
    )

    year_built_min = django_filters.NumberFilter(
        field_name='year_built',
        lookup_expr='gte',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Year'
        })
    )

    garage_spaces = django_filters.NumberFilter(
        field_name='garage_spaces',
        lookup_expr='gte',
        widget=forms.Select(
            choices=[(i, f'{i}+') for i in range(1, 5)],
            attrs={'class': 'form-select'}
        )
    )

    search = django_filters.CharFilter(
        method='filter_search',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search properties...'
        })
    )

    features = django_filters.CharFilter(
        method='filter_features',
        widget=forms.CheckboxSelectMultiple()
    )

    sort_by = django_filters.ChoiceFilter(
        method='filter_sort',
        choices=[
            ('price_asc', 'Price: Low to High'),
            ('price_desc', 'Price: High to Low'),
            ('newest', 'Newest First'),
            ('oldest', 'Oldest First'),
            ('size_asc', 'Size: Small to Large'),
            ('size_desc', 'Size: Large to Small'),
            ('popular', 'Most Popular'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Property
        fields = []

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(description__icontains=value) |
                Q(address__icontains=value) |
                Q(location__name__icontains=value) |
                Q(location__state__icontains=value)
            )
        return queryset

    def filter_features(self, queryset, name, value):
        if value:
            features_list = value.split(',')
            for feature in features_list:
                queryset = queryset.filter(features__contains=[feature.strip()])
        return queryset

    def filter_sort(self, queryset, name, value):
        if value == 'price_asc':
            return queryset.order_by('price')
        elif value == 'price_desc':
            return queryset.order_by('-price')
        elif value == 'newest':
            return queryset.order_by('-created_at')
        elif value == 'oldest':
            return queryset.order_by('created_at')
        elif value == 'size_asc':
            return queryset.order_by('square_feet')
        elif value == 'size_desc':
            return queryset.order_by('-square_feet')
        elif value == 'popular':
            return queryset.order_by('-view_count', '-favorite_count')
        return queryset
