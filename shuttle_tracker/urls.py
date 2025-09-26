from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='shuttle_tracker_home'),
    path('route/<int:route_id>/', views.shuttle_tracker, name='shuttle_tracker'),
    path('route/<int:route_id>/live_locations/', views.live_locations_api, name='live_locations'),
    path('route/<int:route_id>/share_location/', views.share_location_api, name='share_location_api'),
    path('route/<int:route_id>/stop_location/', views.stop_location_api, name='stop_location_api'),
    path('route/<int:route_id>/check_sharing/', views.check_sharing_status, name='check_sharing_status'),
]
