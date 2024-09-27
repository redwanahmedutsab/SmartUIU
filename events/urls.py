from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='event'),
    path('event_post_event/', views.event_post_event_view, name='event_post_event'),
    path('event_edit/<int:id>/', views.event_edit_view, name='event_edit'),
    path('event_delete/<int:id>/', views.event_delete_view, name='event_delete'),
    path('event_registered/', views.event_registered_view, name='event_registered'),
    path('event_posted_event/', views.event_posted_event_view, name='event_posted_event'),
    path('event_single/<int:id>/', views.event_single_view, name='event_single'),
    path('event_send_email/<int:id>/', views.event_send_email_view, name='event_send_email'),
    path('event_registration/<int:id>/', views.event_registration_view,
         name='event_registration'),
]
