from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from qrgenerator.views import qrgenerator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sitestorage.urls')),
    path('qr/', qrgenerator, name='qr-generator'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
