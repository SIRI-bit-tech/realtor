from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.agent_list, name='list'),
    path('agencies/', views.agency_list, name='agency_list'),
    path('agencies/<slug:slug>/', views.agency_detail, name='agency_detail'),
    path('<str:username>/', views.agent_detail, name='agent_detail'),
    path('review/<int:agent_id>/', views.submit_review, name='submit_review'),
    path('contact/<int:agent_id>/', views.contact_agent, name='contact_agent'),
]
