from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('favorites/', views.favorites, name='favorites'),
    path('saved-searches/', views.saved_searches, name='saved_searches'),
    path('save-search/', views.save_search, name='save_search'),
    path('delete-search/<int:search_index>/', views.delete_saved_search, name='delete_saved_search'),
    path('delete-search-model/<int:pk>/', views.delete_saved_search_model, name='delete_saved_search_model'),
    path('notifications/api/', views.notifications_api, name='notifications_api'),
    path('notifications/mark_broadcast_read/<int:notification_id>/', views.mark_broadcast_read, name='mark_broadcast_read'),
    path('<str:username>/', views.profile, name='profile'),
    path('public/<str:username>/', views.public_profile, name='public_profile'),
    path('data-export/', views.data_export, name='data_export'),
]
