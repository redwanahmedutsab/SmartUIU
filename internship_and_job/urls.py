from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='internship_and_job'),
    path('internship_job_post', views.internship_job_post_view, name='internship_job_post'),
    path('job_detail/<int:id>/', views.job_detail_view, name='job_detail'),
    path('internship_job_create_cv', views.internship_job_create_cv_view, name='internship_job_create_cv'),
]
