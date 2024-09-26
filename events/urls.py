from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='event'),
    path('event_post_event/', views.event_post_event_view, name='event_post_event'),
    path('event_posted_event/', views.event_posted_event_view, name='event_posted_event'),
    path('event_single/<int:id>/', views.event_single_view, name='event_single'),
    path('event_send_email/<int:id>/', views.event_send_email_view, name='event_send_email'),
    path('event_registration/<int:id>/', views.event_registration_view,
         name='event_registration'),
]
