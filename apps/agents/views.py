from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from .models import Agent, Agency, AgentReview
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string


def agent_list(request):
    """Agent listings with filtering"""
    agents = Agent.objects.filter(is_active=True).select_related(
        'user', 'agency'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        agents = agents.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(agency__name__icontains=search_query) |
            Q(specializations__contains=[search_query])
        )

    # Filter by agency
    agency_id = request.GET.get('agency')
    if agency_id:
        agents = agents.filter(agency_id=agency_id)

    # Filter by specialization
    specialization = request.GET.get('specialization')
    if specialization:
        agents = agents.filter(specializations__contains=[specialization])

    # Filter by experience
    min_experience = request.GET.get('min_experience')
    if min_experience:
        agents = agents.filter(years_experience__gte=min_experience)

    # Sorting
    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'name':
        agents = agents.order_by('user__first_name', 'user__last_name')
    elif sort_by == 'experience':
        agents = agents.order_by('-years_experience')
    elif sort_by == 'rating':
        agents = agents.order_by('-avg_rating')
    elif sort_by == 'sales':
        agents = agents.order_by('-total_sales')
    else:  # featured
        agents = agents.order_by('-is_featured', '-avg_rating', '-total_sales')

    # Pagination
    paginator = Paginator(agents, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get filter options
    agencies = Agency.objects.all()
    all_specializations = set()
    for agent in Agent.objects.filter(is_active=True):
        if agent.specializations:
            all_specializations.update(agent.specializations)

    context = {
        'page_obj': page_obj,
        'agencies': agencies,
        'specializations': sorted(all_specializations),
        'search_query': search_query,
        'current_agency': agency_id,
        'current_specialization': specialization,
        'current_sort': sort_by,
    }

    if request.htmx:
        return render(request, 'partials/agent_list.html', context)

    return render(request, 'agents/list.html', context)


def agent_detail(request, username):
    """Agent detail page"""
    agent = get_object_or_404(
        Agent.objects.select_related('user', 'agency').annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ),
        user__username=username,
        is_active=True
    )

    # Get agent's recent listings
    recent_listings = agent.user.listings.filter(
        status='available'
    ).select_related('location', 'property_type').prefetch_related('images')[:6]

    # Get reviews
    reviews = agent.reviews.filter(is_verified=True).select_related('reviewer')[:10]

    # Calculate rating distribution
    rating_distribution = {}
    for i in range(1, 6):
        rating_distribution[i] = agent.reviews.filter(rating=i).count()

    context = {
        'agent': agent,
        'recent_listings': recent_listings,
        'reviews': reviews,
        'rating_distribution': rating_distribution,
    }

    return render(request, 'agents/detail.html', context)


def agency_list(request):
    """Agency listings"""
    agencies = Agency.objects.annotate(
        agent_count=Count('agents', filter=Q(agents__is_active=True))
    ).order_by('name')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        agencies = agencies.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(agencies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'agents/agency_list.html', context)


def agency_detail(request, slug):
    """Agency detail page"""
    agency = get_object_or_404(Agency, slug=slug)

    # Get agency agents
    agents = agency.agents.filter(is_active=True).select_related('user').annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )

    # Get agency statistics
    total_listings = 0
    total_sales = 0
    for agent in agents:
        total_listings += agent.listings.filter(status='available').count()
        total_sales += agent.total_sales

    context = {
        'agency': agency,
        'agents': agents,
        'total_listings': total_listings,
        'total_sales': total_sales,
    }

    return render(request, 'agents/agency_detail.html', context)


@require_http_methods(["POST"])
def submit_review(request, agent_id):
    """Submit agent review via HTMX"""
    if not request.user.is_authenticated:
        return render(request, 'partials/login_required.html')

    agent = get_object_or_404(Agent, id=agent_id)

    # Check if user already reviewed this agent
    existing_review = AgentReview.objects.filter(
        agent=agent, reviewer=request.user
    ).first()

    if existing_review:
        return render(request, 'partials/review_error.html', {
            'message': 'You have already reviewed this agent.'
        })

    rating = request.POST.get('rating')
    title = request.POST.get('title')
    comment = request.POST.get('comment')

    if not all([rating, title, comment]):
        return render(request, 'partials/review_error.html', {
            'message': 'All fields are required.'
        })

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except (ValueError, TypeError):
        return render(request, 'partials/review_error.html', {
            'message': 'Invalid rating value.'
        })

    # Create review
    review = AgentReview.objects.create(
        agent=agent,
        reviewer=request.user,
        rating=rating,
        title=title,
        comment=comment
    )

    # Update agent's average rating
    agent.average_rating = agent.reviews.aggregate(
        avg_rating=Avg('rating')
    )['avg_rating'] or 0
    agent.save(update_fields=['average_rating'])

    return render(request, 'partials/review_success.html', {
        'review': review
    })


@require_http_methods(["POST"])
@csrf_exempt  # If you use HTMX, ensure CSRF is handled or exempted
def contact_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    message = request.POST.get('message', '').strip()

    if not all([name, email, message]):
        return render(request, 'partials/contact_error.html', {'message': 'All fields are required.'})

    subject = f"New message from {name} via Nuvana Realty Agent Contact"
    context = {
        'name': name,
        'email': email,
        'phone': phone,
        'message': message,
        'agent': agent,
        'site_url': request.build_absolute_uri('/'),
        'logo_url': request.build_absolute_uri('/static/images/logo.png'),
    }
    html_message = render_to_string('emails/agent_contact.html', context)
    plain_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
    recipient = [agent.user.email]
    try:
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=False, html_message=html_message)
        return render(request, 'partials/contact_success.html', {'name': name})
    except Exception as e:
        return render(request, 'partials/contact_error.html', {'message': 'Failed to send message. Please try again later.'})

