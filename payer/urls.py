from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='payer_home'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('ssl-payment-init/', views.ssl_payment_init, name='ssl_payment_init'),
    path('ssl-success/', views.ssl_payment_success, name='ssl_payment_success'),
    path('ssl-fail/', views.ssl_payment_fail, name='ssl_payment_fail'),
    path('ssl-cancel/', views.ssl_payment_cancel, name='ssl_payment_cancel'),
    path('receipt/<int:payment_id>/', views.generate_receipt, name='generate_receipt'),
]
