from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='study_group'),
    path('study_group_create_group/', views.study_group_create_group_view, name='study_group_create_group'),
    path('study_group_chat/<int:id>/', views.study_group_chat_view, name='study_group_chat'),
    path('edit_members/<int:id>/', views.edit_members, name='edit_members'),
    path('delete_group/<int:group_id>/', views.delete_group_view, name='delete_group'),
]
