from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='internship_and_job'),
]
