from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('<slug:slug>/', views.property_detail, name='detail'),
    path('favorite/<uuid:property_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('api/map-data/', views.property_map_data, name='map_data'),
]
