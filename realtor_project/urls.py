from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseBadRequest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('properties/', include('apps.properties.urls', namespace='properties')),
    path('agents/', include('apps.agents.urls', namespace='agents')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('search/', include('apps.search.urls', namespace='search')),
    path('messaging/', include('apps.messaging.urls', namespace='messaging')),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),  # Add this line
    # Catch HTTP requests to WebSocket endpoints and return 400
    re_path(r'^ws/messaging/.*$', lambda request: HttpResponseBadRequest('WebSocket endpoint: use a WebSocket connection, not HTTP.')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)