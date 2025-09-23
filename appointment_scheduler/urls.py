# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='appointment_scheduler'),
    path('faculty/set_schedule/', views.faculty_set_schedule, name='faculty_set_schedule'),
    path('appointment_scheduler/faculty_data/', views.faculty_routine, name='faculty_data'),

    path('faculty/create_profile/', views.faculty_create_profile, name='faculty_profile_create'),
    path('faculty/manage_schedule/', views.faculty_manage_schedule, name='faculty_manage_schedule'),

    path('appointments/book/<int:faculty_id>/', views.book_appointment_student, name='appointment_booking_student'),
    path('my-bookings/', views.student_bookings, name='student_bookings'),
    path('remove-booking/<int:booking_id>/', views.remove_booking, name='remove_booking'),
]
