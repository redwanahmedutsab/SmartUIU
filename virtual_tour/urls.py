from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_home, name='virtual_tour_home'),
    path('loaction/<int:location_id>/', views.virtual_tour, name='virtual_tour'),
]
