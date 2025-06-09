from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from apps.properties.models import Property, Location, PropertyType
from apps.agents.models import Agent


def search_results(request):
    """Main search results page"""
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    property_type = request.GET.get('property_type', '')
    listing_type = request.GET.get('listing_type', '')

    # Start with all available properties
    properties = Property.objects.filter(status='available').select_related(
        'location', 'property_type', 'agent'
    ).prefetch_related('images')

    # Apply search filters
    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )

    if location:
        properties = properties.filter(
            Q(location__name__icontains=location) |
            Q(location__state__icontains=location) |
            Q(address__icontains=location)
        )

    if property_type:
        properties = properties.filter(property_type__slug=property_type)

    if listing_type:
        properties = properties.filter(listing_type=listing_type)

    # Pagination
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'location': location,
        'property_type': property_type,
        'listing_type': listing_type,
        'total_results': properties.count(),
    }

    if request.htmx:
        return render(request, 'partials/search_results.html', context)

    return render(request, 'search/results.html', context)


def search_suggestions(request):
    """HTMX endpoint for search autocomplete"""
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    # Search in properties
    property_suggestions = Property.objects.filter(
        Q(title__icontains=query) | Q(address__icontains=query),
        status='available'
    ).values('title', 'slug', 'address')[:5]

    # Search in locations
    location_suggestions = Location.objects.filter(
        Q(name__icontains=query) | Q(state__icontains=query)
    ).values('name', 'slug', 'state')[:5]

    # Search in agents
    agent_suggestions = Agent.objects.filter(
        Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query),
        is_active=True
    ).select_related('user').values(
        'user__first_name', 'user__last_name', 'user__username'
    )[:3]

    suggestions = {
        'properties': list(property_suggestions),
        'locations': list(location_suggestions),
        'agents': list(agent_suggestions),
    }

    if request.htmx:
        return render(request, 'partials/search_suggestions.html', {
            'suggestions': suggestions,
            'query': query
        })

    return JsonResponse(suggestions)
