from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, F, Q
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta

from .models import PageView, PropertyView, SearchQuery, UserActivity
from apps.properties.models import Property

@login_required
def analytics_dashboard(request):
    """Main analytics dashboard view"""
    # Only staff/admin users can access analytics
    if not request.user.is_staff:
        return render(request, 'analytics/access_denied.html')
    
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Basic stats
    total_page_views = PageView.objects.filter(timestamp__gte=start_date).count()
    total_property_views = PropertyView.objects.filter(timestamp__gte=start_date).count()
    total_searches = SearchQuery.objects.filter(timestamp__gte=start_date).count()
    
    # Most viewed properties - using a different annotation name
    most_viewed_properties = Property.objects.filter(
        analytics_views__timestamp__gte=start_date
    ).annotate(
        analytics_view_count=Count('analytics_views')
    ).order_by('-analytics_view_count')[:10]
    
    # Most searched terms
    most_searched_terms = SearchQuery.objects.filter(
        timestamp__gte=start_date
    ).values('query').annotate(
        search_count=Count('id')
    ).order_by('-search_count')[:10]
    
    # User activity by type
    user_activities = UserActivity.objects.filter(
        timestamp__gte=start_date
    ).values('action').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Daily page views for chart
    daily_views = PageView.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        day=TruncDay('timestamp')
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    context = {
        'total_page_views': total_page_views,
        'total_property_views': total_property_views,
        'total_searches': total_searches,
        'most_viewed_properties': most_viewed_properties,
        'most_searched_terms': most_searched_terms,
        'user_activities': user_activities,
        'daily_views': list(daily_views),
        'days': days,
    }
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
def property_analytics(request):
    """Property-specific analytics view"""
    if not request.user.is_staff:
        return render(request, 'analytics/access_denied.html')
    
    # Get property ID from request
    property_id = request.GET.get('property_id')
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    if property_id:
        # Get property details
        try:
            property = Property.objects.get(id=property_id)
            
            # Get view statistics - using the correct related name
            views = PropertyView.objects.filter(
                property=property,
                timestamp__gte=start_date
            )
            
            daily_views = views.annotate(
                day=TruncDay('timestamp')
            ).values('day').annotate(
                count=Count('id')
            ).order_by('day')
            
            # Get user activities related to this property
            activities = UserActivity.objects.filter(
                property=property,
                timestamp__gte=start_date
            ).values('action').annotate(
                count=Count('id')
            ).order_by('-count')
            
            context = {
                'property': property,
                'view_count': views.count(),
                'daily_views': list(daily_views),
                'activities': activities,
                'days': days,
            }
            
            return render(request, 'analytics/property_detail.html', context)
            
        except Property.DoesNotExist:
            pass
    
    # If no property ID or invalid ID, show list of properties with analytics
    properties = Property.objects.annotate(
        analytics_view_count=Count('analytics_views', filter=Q(analytics_views__timestamp__gte=start_date))
    ).order_by('-analytics_view_count')
    
    context = {
        'properties': properties,
        'days': days,
    }
    
    return render(request, 'analytics/property_list.html', context)

@login_required
def search_analytics(request):
    """Search analytics view"""
    if not request.user.is_staff:
        return render(request, 'analytics/access_denied.html')
    
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # Most searched terms
    most_searched = SearchQuery.objects.filter(
        timestamp__gte=start_date
    ).values('query').annotate(
        search_count=Count('id'),
        avg_results=Avg('results_count')
    ).order_by('-search_count')[:20]
    
    # Zero result searches
    zero_results = SearchQuery.objects.filter(
        timestamp__gte=start_date,
        results_count=0
    ).values('query').annotate(
        search_count=Count('id')
    ).order_by('-search_count')[:20]
    
    # Search trends over time
    daily_searches = SearchQuery.objects.filter(
        timestamp__gte=start_date
    ).annotate(
        day=TruncDay('timestamp')
    ).values('day').annotate(
        count=Count('id'),
        avg_results=Avg('results_count')
    ).order_by('day')
    
    context = {
        'most_searched': most_searched,
        'zero_results': zero_results,
        'daily_searches': list(daily_searches),
        'days': days,
    }
    
    return render(request, 'analytics/search.html', context)

@login_required
def export_analytics(request):
    """Export analytics data as JSON"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    data_type = request.GET.get('type', 'pageviews')
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    if data_type == 'pageviews':
        data = list(PageView.objects.filter(
            timestamp__gte=start_date
        ).values('url', 'timestamp', 'user__username', 'ip_address'))
    
    elif data_type == 'property_views':
        data = list(PropertyView.objects.filter(
            timestamp__gte=start_date
        ).values('property__title', 'timestamp', 'user__username', 'ip_address'))
    
    elif data_type == 'searches':
        data = list(SearchQuery.objects.filter(
            timestamp__gte=start_date
        ).values('query', 'results_count', 'timestamp', 'user__username'))
    
    elif data_type == 'user_activity':
        data = list(UserActivity.objects.filter(
            timestamp__gte=start_date
        ).values('user__username', 'action', 'property__title', 'timestamp'))
    
    else:
        data = {'error': 'Invalid data type'}
    
    return JsonResponse({'data': data})
