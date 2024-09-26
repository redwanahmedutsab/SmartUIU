# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verification/', views.verification_view, name='verification'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('developers/', views.developers_view, name='developers'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('forget_email/', views.forget_email_view, name='forget_email'),
    path('forget_code/', views.forget_code_view, name='forget_code'),
    path('forget_new/', views.forget_new_view, name='forget_new'),
    path('logout/', views.logout_view, name='logout'),
]
