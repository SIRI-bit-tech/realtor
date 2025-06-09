from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count, Avg, Min, Max
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyType, Location, PropertyFavorite, PropertyView
from .filters import PropertyFilter


def property_list(request):
    """Property listings with HTMX filtering"""
    properties = Property.objects.filter(status='available').select_related(
        'location', 'property_type', 'agent'
    ).prefetch_related('images')

    # Apply filters
    property_filter = PropertyFilter(request.GET, queryset=properties)
    filtered_properties = property_filter.qs

    # Pagination
    paginator = Paginator(filtered_properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    property_types = PropertyType.objects.all()
    locations = Location.objects.all()
    price_range = properties.aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )

    context = {
        'page_obj': page_obj,
        'filter': property_filter,
        'property_types': property_types,
        'locations': locations,
        'price_range': price_range,
    }

    if request.htmx:
        return render(request, 'partials/property_list.html', context)

    return render(request, 'properties/list.html', context)


def property_detail(request, slug):
    """Property detail page with image gallery and virtual tour"""
    property_obj = get_object_or_404(
        Property.objects.select_related(
            'location', 'property_type', 'agent', 'agent__agency'
        ).prefetch_related('images'),
        slug=slug
    )

    # Record property view
    if request.user.is_authenticated:
        PropertyView.objects.get_or_create(
            property=property_obj,
            user=request.user,
            defaults={
                'ip_address': request.META.get('REMOTE_ADDR', ''),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
        )

    # Update view count
    property_obj.view_count += 1
    property_obj.save(update_fields=['view_count'])

    # Similar properties
    similar_properties = Property.objects.filter(
        location=property_obj.location,
        property_type=property_obj.property_type,
        status='available'
    ).exclude(id=property_obj.id)[:4]

    # Check if user has favorited this property
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = PropertyFavorite.objects.filter(
            user=request.user,
            property=property_obj
        ).exists()

    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
        'is_favorited': is_favorited,
    }

    return render(request, 'properties/detail.html', context)


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, property_id):
    """HTMX endpoint to toggle property favorite"""
    property_obj = get_object_or_404(Property, id=property_id)

    favorite, created = PropertyFavorite.objects.get_or_create(
        user=request.user,
        property=property_obj
    )

    if not created:
        favorite.delete()
        is_favorited = False
        # Update favorite count
        property_obj.favorite_count = max(0, property_obj.favorite_count - 1)
    else:
        is_favorited = True
        property_obj.favorite_count += 1

    property_obj.save(update_fields=['favorite_count'])

    context = {
        'property': property_obj,
        'is_favorited': is_favorited,
    }

    return render(request, 'partials/favorite_button.html', context)


@require_http_methods(["GET"])
def property_map_data(request):
    """API endpoint for map markers"""
    properties = Property.objects.filter(
        status='available',
        latitude__isnull=False,
        longitude__isnull=False
    ).values(
        'id', 'title', 'slug', 'price', 'latitude', 'longitude',
        'bedrooms', 'bathrooms', 'square_feet'
    )

    markers = []
    for prop in properties:
        markers.append({
            'id': str(prop['id']),
            'title': prop['title'],
            'url': f"/properties/{prop['slug']}/",
            'price': float(prop['price']),
            'lat': float(prop['latitude']),
            'lng': float(prop['longitude']),
            'bedrooms': prop['bedrooms'],
            'bathrooms': float(prop['bathrooms']),
            'square_feet': prop['square_feet'],
        })

    return JsonResponse({'markers': markers})
