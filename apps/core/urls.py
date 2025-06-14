from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('privacy/', views.privacy_policy, name='privacy'),
]
