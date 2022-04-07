
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path

from . import views
from stock.views import ContractorUpdateView, ContractorDetailView

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('detail/<int:pk>', views.UserDetailView.as_view(), name='detail-user'),
    path('change-password/<int:id>', views.password_change, name='change-password'),
    path('customer/create/', views.CustomerCreateView.as_view() , name='create-customer'),
    path('customer/detail/<int:pk>', views.CustomerDetailView.as_view() , name='detail-customer'),
    path('customer/update/<int:pk>', views.CustomerUpdateView.as_view() , name='update-customer'),
    path('customer/list', views.CustomerListView.as_view(), name='list-customer'),
    path('contracotr/edit/<int:pk>', ContractorUpdateView.as_view(), name='update-contractor'),
    path('contracotr/detail/<int:pk>', ContractorDetailView.as_view(), name='detail-contractor'),
]
