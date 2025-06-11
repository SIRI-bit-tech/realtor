from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversations/', views.conversation_list, name='conversation_list'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversations/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversations/<int:conversation_id>/mark-read/', views.mark_conversation_read, name='mark_read'),
    path('start/', views.start_conversation, name='start_conversation'),
]
