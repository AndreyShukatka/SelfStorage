from django.urls import path
from sitestorage import views


urlpatterns = [
    path('', views.index, name='index'),
    path('boxes', views.boxes, name='boxes'),
    path('faq', views.faq, name='faq'),
    path('my-rent', views.my_rent, name='my_rent'),
]

