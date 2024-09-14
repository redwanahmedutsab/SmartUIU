from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('homepage.urls')),
    path('lost_and_found/', include('lost_and_found.urls')),  # New lost_and_found app
    path('thesis_finder/', include('thesis_finder.urls')),  # New lost_and_found app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
