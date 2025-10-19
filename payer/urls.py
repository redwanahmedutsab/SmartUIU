from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='payer_home'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('bkash-payment/', views.bkash_payment, name='bkash_payment'),
    path('receipt/<int:payment_id>/', views.generate_receipt, name='generate_receipt'),
]