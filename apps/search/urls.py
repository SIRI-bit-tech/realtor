from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_results, name='results'),
    path('suggestions/', views.search_suggestions, name='suggestions'),
]
