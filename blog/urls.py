from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog'),
    path('blog_my_blog/', views.blog_my_blog_view, name='blog_my_blog'),
    path('blog_single/<int:id>//', views.blog_single_view, name='blog_single'),
    path('blog_post/', views.blog_post_view, name='blog_post'),
    path('delete/<int:id>/', views.blog_delete_view, name='blog_delete'),
    path('blog/edit/<int:blog_id>/', views.edit_blog, name='blog_edit'),
]
