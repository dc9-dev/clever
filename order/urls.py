from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('order/new/', views.new, name='new'),
    path('order/edit/<slug:slug>/', views.edit, name='edit'),
    path('order/edit/<slug:slug>/deleteitem/<item_id>', views.deleteItem, name='deleteItem'),
    path('order/<slug:slug>/', views.detail, name='detail'),
    path('order/<slug:slug>/export_csv', views.export_csv, name='export_csv'),
    path('order/<slug:slug>/export_pdf', views.export_pdf, name='export_pdf'),

]
