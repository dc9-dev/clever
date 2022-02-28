from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductionHome, name='home-production'),
    path('new/', views.CreateProduction, name='create-production'),
    path('<int:id>/edit', views.EditProduction, name='edit-production'),
    path('<int:id>/detail', views.DetailProduction, name='detail-production'),
    path('<int:id>/filter', views.ProductionStockFilter, name='production-filter'),
    path('<int:id>/stockin', views.ProductionStockIn, name='stockin'),
    path('comments/<int:id>', views.ProductionComments, name='comments'),
    path('status/<int:id>', views.ProductionStatus, name='status'),
    path('orders/' views.HomeOrders, name='home-orders'),
]
