from django.utils import timezone
from .models import PageView

class AnalyticsMiddleware:
    """Middleware to track page views"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        response = self.get_response(request)
        
        # Skip tracking for static files, admin, and AJAX requests
        if (
            request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path.startswith('/admin/') or
            request.headers.get('HX-Request') == 'true' or
            request.path.startswith('/analytics/')  # Don't track analytics pages
        ):
            return response
        
        # Record the page view
        try:
            PageView.objects.create(
                url=request.build_absolute_uri(),
                path=request.path,
                query_params=dict(request.GET.items()),
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', ''),
                timestamp=timezone.now()
            )
        except Exception as e:
            # Log the error but don't interrupt the response
            print(f"Analytics error: {e}")
        
        return response
    
    def get_client_ip(self, request):
        """Get the client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
