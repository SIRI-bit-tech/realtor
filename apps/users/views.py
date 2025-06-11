from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from apps.properties.models import Property, PropertyFavorite
from .models import UserProfile
from apps.messaging.models import Conversation, Message

User = get_user_model()

@login_required
def dashboard(request):
    """User dashboard"""
    user = request.user
    
    # Get user's favorite properties
    favorites = PropertyFavorite.objects.filter(user=user).select_related(
        'property__location', 'property__property_type'
    ).prefetch_related('property__images')[:6]
    
    # Get recent property views using the correct related name
    recent_views = user.property_views.select_related(
        'property__location', 'property__property_type'
    ).prefetch_related('property__images').order_by('-created_at')[:6]
    
    # Get saved searches count - handle if profile doesn't exist
    try:
        profile = user.profile
        saved_searches_count = len(profile.saved_searches) if profile.saved_searches else 0
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=user)
        saved_searches_count = 0
    
    # Unread messages count
    unread_messages_count = Message.objects.filter(
        Q(conversation__participants=user) & ~Q(sender=user),
        is_read=False
    ).count()
    
    # Dashboard statistics
    stats = {
        'favorites_count': favorites.count(),
        'views_count': recent_views.count(),
        'saved_searches_count': saved_searches_count,
    }
    
    context = {
        'favorites': favorites,
        'recent_views': recent_views,
        'stats': stats,
        'unread_messages_count': unread_messages_count,
    }
    
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request, username):
    """User profile page"""
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = request.user == profile_user
    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
    }
    if is_own_profile:
        # Get user's favorite properties
        favorites = PropertyFavorite.objects.filter(user=profile_user).select_related(
            'property__location', 'property__property_type'
        ).prefetch_related('property__images')[:6]
        # Get recent property views
        recent_views = profile_user.property_views.select_related(
            'property__location', 'property__property_type'
        ).prefetch_related('property__images').order_by('-created_at')[:6]
        # Get saved searches count
        try:
            profile = profile_user.profile
            saved_searches_count = len(profile.saved_searches) if profile.saved_searches else 0
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=profile_user)
            saved_searches_count = 0
        # Unread messages count
        unread_messages_count = Message.objects.filter(
            Q(conversation__participants=profile_user) & ~Q(sender=profile_user),
            is_read=False
        ).count()
        stats = {
            'favorites_count': favorites.count(),
            'views_count': recent_views.count(),
            'saved_searches_count': saved_searches_count,
        }
        context.update({
            'favorites': favorites,
            'recent_views': recent_views,
            'stats': stats,
            'unread_messages_count': unread_messages_count,
        })
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        user = request.user
        
        # Get or create profile
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)
        
        # Update user fields
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.bio = request.POST.get('bio', '')
        user.location = request.POST.get('location', '')
        user.website = request.POST.get('website', '')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        
        user.save()
        
        # Update profile fields
        profile.preferred_contact = request.POST.get('preferred_contact', 'email')
        
        budget_min = request.POST.get('budget_min')
        if budget_min:
            try:
                profile.budget_min = float(budget_min)
            except ValueError:
                profile.budget_min = None
        
        budget_max = request.POST.get('budget_max')
        if budget_max:
            try:
                profile.budget_max = float(budget_max)
            except ValueError:
                profile.budget_max = None
        
        # Handle preferred locations (JSON field)
        preferred_locations = request.POST.getlist('preferred_locations')
        profile.preferred_locations = preferred_locations
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        
        if request.htmx:
            return render(request, 'partials/profile_success.html')
        
        return redirect('users:profile', username=user.username)
    
    return render(request, 'users/edit_profile.html')

@login_required
def favorites(request):
    """User's favorite properties"""
    favorites = PropertyFavorite.objects.filter(user=request.user).select_related(
        'property__location', 'property__property_type', 'property__agent'
    ).prefetch_related('property__images').order_by('-created_at')
    
    # Search in favorites
    search_query = request.GET.get('search', '')
    if search_query:
        favorites = favorites.filter(
            Q(property__title__icontains=search_query) |
            Q(property__address__icontains=search_query) |
            Q(property__location__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'users/favorites.html', context)

@login_required
def saved_searches(request):
    """User's saved searches"""
    try:
        profile = request.user.profile
        saved_searches = profile.saved_searches or []
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        profile = UserProfile.objects.create(user=request.user)
        saved_searches = []
    
    context = {
        'saved_searches': saved_searches,
    }
    
    return render(request, 'users/saved_searches.html', context)

@login_required
@require_http_methods(["POST"])
def save_search(request):
    """Save current search parameters"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    search_params = {
        'name': request.POST.get('search_name', 'Untitled Search'),
        'params': dict(request.POST),
        'created_at': timezone.now().isoformat(),
    }
    
    if not profile.saved_searches:
        profile.saved_searches = []
    
    profile.saved_searches.append(search_params)
    profile.save()
    
    messages.success(request, 'Search saved successfully!')
    
    if request.htmx:
        return render(request, 'partials/search_saved.html', {
            'search': search_params
        })
    
    return redirect('users:saved_searches')

@login_required
@require_http_methods(["POST"])
def delete_saved_search(request, search_index):
    """Delete a saved search"""
    try:
        profile = request.user.profile
        
        if profile.saved_searches and 0 <= search_index < len(profile.saved_searches):
            del profile.saved_searches[search_index]
            profile.save()
            messages.success(request, 'Saved search deleted!')
    except UserProfile.DoesNotExist:
        pass
    
    if request.htmx:
        return render(request, 'partials/search_deleted.html')
    
    return redirect('users:saved_searches')

def public_profile(request, username):
    """Public profile view (for non-authenticated users)"""
    user = get_object_or_404(User, username=username)
    
    # Only show public information
    context = {
        'profile_user': user,
        'is_public_view': True,
    }
    
    # If it's an agent, show agent information
    if hasattr(user, 'agent') and user.agent and user.agent.is_active:
        agent = user.agent
        recent_listings = agent.listings.filter(
            status='available'
        ).select_related('location', 'property_type').prefetch_related('images')[:6]
        
        context.update({
            'agent': agent,
            'recent_listings': recent_listings,
        })
        return render(request, 'users/public_agent_profile.html', context)
    
    return render(request, 'users/public_profile.html', context)
