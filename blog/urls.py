from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog'),
    path('blog_my_blog/', views.blog_my_blog_view, name='blog_my_blog'),
    path('blog_notification/', views.blog_notification, name='blog_notification'),
    path('blog_single/<int:id>//', views.blog_single_view, name='blog_single'),
    path('blog_post/', views.blog_post_view, name='blog_post'),
    path('delete/<int:id>/', views.blog_delete_view, name='blog_delete'),
    path('blog/edit/<int:blog_id>/', views.edit_blog, name='blog_edit'),
    path('comment_delete/<int:id>/', views.comment_delete, name='comment_delete'),
    path('reply_delete/<int:id>/', views.reply_delete, name='reply_delete'),  # URL for reply deletion
    path('blog/<int:blog_id>/toggle_reaction/', views.toggle_reaction, name='toggle_reaction'),
    path('tag_search/<str:tag_name>/', views.tag_search, name='tag_search'),
    path('notifications/mark-all-read/', views.mark_all_as_read, name='mark_all_read'),

]
