# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='thesis_finder'),
    path('thesis_finder_create_profile/', views.thesis_member_create_profile_view, name='thesis_finder_create_profile'),
    path('thesis_finder_single/<int:id>//', views.thesis_member_single_view, name='thesis_finder_single'),
    path('thesis_finder_profile/', views.thesis_finder_profile_view, name='thesis_finder_profile'),
]
