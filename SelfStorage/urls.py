from django.contrib import admin
from django.urls import path, include
from qrgenerator.views import qrgenerator

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sitestorage.urls')),
    path('qr/', qrgenerator, name='qr-generator'),
]
