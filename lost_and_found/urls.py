from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='lost_and_found'),
    path('lost_and_found_register/', views.lost_and_found_register_view, name='lost_and_found_register'),
    path('lost_and_found_user_section/', views.lost_and_found_user_section_view, name='lost_and_found_user_section'),
    path('lost_and_found_single/<int:id>/', views.lost_and_found_single_view, name='lost_and_found_single'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
