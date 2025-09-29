from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='digital_desk_home'),
    path('add-routine/', views.add_class_routine, name='add_class_routine'),
    path('add-note/', views.add_note, name='add_note'),
    path('add-task/', views.add_task, name='add_task'),
    path('toggle-task/<int:task_id>/', views.toggle_task, name='task_toggle'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('add_reminder/', views.add_reminder, name='add_reminder'),
    path('delete-reminder/<int:reminder_id>/', views.delete_reminder, name='delete_reminder'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('edit-note/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete-routine/<int:pk>/', views.delete_routine, name='delete_routine'),

]
