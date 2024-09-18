from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='marketplace'),
    path('marketplace_post/', views.marketplace_post_view, name='marketplace_post'),
    path('marketplace_my_post/', views.marketplace_my_post_view, name='marketplace_my_post'),
    path('marketplace_single/<int:product_id>/', views.marketplace_single_view, name='marketplace_single'),
    path('marketplace/<int:product_id>/edit/', views.marketplace_edit_view, name='marketplace_edit'),
]
