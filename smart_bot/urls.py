from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='smart_bot_home'),
    path('new/', views.new_chat, name='new_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/<int:chat_id>/message/', views.chat_message, name='chat_message'),
    path("chat/<int:chat_id>/delete/", views.delete_chat, name="delete_chat"),

]
