from django.urls import path
from sitestorage import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('boxes/', views.BoxesListView.as_view(), name='boxes'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('my-rent/', views.ProfileView.as_view(), name='my_rent'),
    path('call-modal/', views.get_modal_window, name='modal'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('pay/<int:pk>/', views.pay, name='pay'),
    path('confirm_pay/<int:pk>', views.confirm_pay, name='confirm_pay')
]
