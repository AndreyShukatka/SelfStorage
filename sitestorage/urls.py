from django.urls import path
from sitestorage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('boxes', views.boxes, name='boxes'),
    path('faq', views.faq, name='faq'),
    path('my-rent', views.my_rent, name='my_rent'),
    path('my-rent-empty', views.my_rent_empty, name='my_rent_empty')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
