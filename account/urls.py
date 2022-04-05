
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path

from . import views


urlpatterns = [
    path('', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('detail/<int:pk>', views.UserDetailView.as_view(), name='detail-user'),
    path('change-password/<int:id>', views.password_change, name='change-password'),
    path('customer/create/', views.CustomerCreateView.as_view() , name='create-customer'),
    path('customer/detail/<int:id>', views.CustomerDetailView.as_view() , name='detail-customer'),
]
