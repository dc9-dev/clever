from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.new, name='new'),
    path('edit/<slug:slug>/', views.edit, name='edit'),
    path('edit/<slug:slug>/deleteitem/<item_id>', views.deleteItem, name='deleteItem'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('<slug:slug>/export', views.export_csv, name='export_csv'),
]
