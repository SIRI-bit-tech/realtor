from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    path('properties/', views.property_analytics, name='properties'),
    path('searches/', views.search_analytics, name='searches'),
    path('export/', views.export_analytics, name='export'),
]
