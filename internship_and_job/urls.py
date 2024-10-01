from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='internship_and_job'),
    path('internship_job_post/', views.internship_job_post_view, name='internship_job_post'),
    path('internship_job_posted_jobs/', views.internship_job_posted_jobs_view, name='internship_job_posted_jobs'),
    path('internship_job_applied_jobs/', views.internship_job_applied_jobs_view, name='internship_job_applied_jobs'),
    path('internship_job_single/<int:id>/', views.internship_job_single_view, name='internship_job_single'),
    path('internship_job_applied_candidate/<int:id>/', views.internship_job_applied_candidate_view,
         name='internship_job_applied_candidate'),
    path('internship_job_edit/<int:id>/', views.internship_job_edit_view, name='internship_job_edit'),
    path('internship_job_edit_job/<int:id>/', views.internship_job_edit_job_view, name='internship_job_edit_job'),
    path('internship_job_edit_cv/', views.internship_job_edit_cv_view, name='internship_job_edit_cv'),
    path('internship_job_edit_cv_id/<int:id>/', views.internship_job_edit_cv_id_view, name='internship_job_edit_cv_id'),
    path('internship_job_view_cv/<int:id>/', views.internship_job_view_cv_view, name='internship_job_view_cv'),
    path('internship_job_delete_job/<int:id>/', views.internship_job_delete_job_view, name='internship_job_delete_job'),
    path('internship_job_create_cv/', views.internship_job_create_cv_view, name='internship_job_create_cv'),
    path('delete_cv/<int:cv_id>/', views.delete_cv, name='delete_cv'),

]
