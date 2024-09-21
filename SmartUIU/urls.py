from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('homepage.urls')),
    path('lost_and_found/', include('lost_and_found.urls')),
    path('thesis_finder/', include('thesis_finder.urls')),
    path('blog/', include('blog.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('course_materials_and_feedback/', include('course_materials_and_feedback.urls')),
    path('homefinder/', include('homefinder.urls')),
    path('internship_and_job/', include('internship_and_job.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
