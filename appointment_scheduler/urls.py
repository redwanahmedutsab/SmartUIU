# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='appointment_scheduler'),
    path('appointments/book/<int:faculty_id>/', views.book_appointment_student, name='appointment_booking_student'),
    path('my-bookings/', views.student_bookings, name='student_bookings'),
    path('remove-booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
]
