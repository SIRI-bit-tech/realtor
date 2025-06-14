from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from apps.properties.models import Property, PropertyType, Location
from apps.agents.models import Agent, Agency
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def home(request):
    """Landing page with parallax and animations"""
    # Featured properties
    featured_properties = Property.objects.filter(
        status='available'
    ).select_related('location', 'property_type', 'agent').prefetch_related('images')[:6]

    # Statistics for counter animations
    stats = {
        'total_properties': Property.objects.filter(status='available').count(),
        'total_agents': Agent.objects.filter(is_active=True).count(),
        'total_sales': Property.objects.filter(status='sold').count(),
        'total_locations': Location.objects.count(),
    }

    # Featured agents
    featured_agents = Agent.objects.filter(
        is_featured=True, is_active=True
    ).select_related('user', 'agency')[:4]

    # Property types for search
    property_types = PropertyType.objects.all()
    locations = Location.objects.all()[:10]  # Top 10 locations

    context = {
        'featured_properties': featured_properties,
        'stats': stats,
        'featured_agents': featured_agents,
        'property_types': property_types,
        'locations': locations,
    }

    return render(request, 'pages/home.html', context)


@cache_page(60 * 15)  # Cache for 15 minutes
def about(request):
    """About page with team and company info"""
    team_members = Agent.objects.filter(
        is_featured=True, is_active=True
    ).select_related('user', 'agency')

    agencies = Agency.objects.all()[:6]

    context = {
        'team_members': team_members,
        'agencies': agencies,
    }

    return render(request, 'pages/about.html', context)


def contact(request):
    """Contact page with form and map"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if not all([name, email, message]):
            if request.htmx:
                return render(request, 'partials/contact_error.html', {'message': 'All fields are required.'})
            return render(request, 'pages/contact.html', {'error': 'All fields are required.'})

        subject = f"New Contact Message from {name}"
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
            'site_url': request.build_absolute_uri('/'),
            'logo_url': request.build_absolute_uri('/static/images/logo.png'),
        }
        html_message = render_to_string('emails/general_contact.html', context)
        plain_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        recipient = [getattr(settings, 'CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)]
        try:
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=False, html_message=html_message)
            if request.htmx:
                return render(request, 'partials/contact_success.html', {'name': name})
            return render(request, 'pages/contact.html', {'success': True, 'name': name})
        except Exception as e:
            if request.htmx:
                return render(request, 'partials/contact_error.html', {'message': 'Failed to send message. Please try again later.'})
            return render(request, 'pages/contact.html', {'error': 'Failed to send message. Please try again later.'})
    return render(request, 'pages/contact.html')


@require_http_methods(["GET"])
def search_suggestions(request):
    """HTMX endpoint for search autocomplete"""
    query = request.GET.get('q', '').strip()

    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    # Search in properties and locations
    property_suggestions = Property.objects.filter(
        Q(title__icontains=query) | Q(address__icontains=query),
        status='available'
    ).values('title', 'slug')[:5]

    location_suggestions = Location.objects.filter(
        Q(name__icontains=query) | Q(state__icontains=query)
    ).values('name', 'slug')[:5]

    suggestions = {
        'properties': list(property_suggestions),
        'locations': list(location_suggestions),
    }

    if request.htmx:
        return render(request, 'partials/search_suggestions.html', {
            'suggestions': suggestions
        })

    return JsonResponse(suggestions)


def privacy_policy(request):
    return render(request, 'pages/privacy.html')

