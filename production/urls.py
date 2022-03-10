from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductionHome, name='home-production'),
    path('new/<int:id>', views.CreateProduction, name='create-production'),
    path('<int:id>/edit', views.EditProduction, name='edit-production'),
    path('<int:id>/increment', views.ProductionMaterialIncrement, name='increment'),
    path('<int:id>/decrement', views.ProductionMaterialDecrement, name='decrement'),
    path('<int:id>/detail', views.DetailProduction, name='detail-production'),
    path('<int:id>/filter', views.ProductionStockFilter, name='production-filter'),
    path('<int:id>/stockin', views.ProductionStockIn, name='stockin'),
    path('comments/<int:id>', views.ProductionComments, name='comments'),
    path('status/<int:id>', views.ProductionStatus, name='status'),
    path('orders/', views.HomeOrders, name='home-orders'),
    path('orders/create', views.CreateOrder, name='create-order'),
    path('orders/edit/<int:id>', views.EditOrder, name='edit-order'),
    path('orders/detail/<int:id>', views.DetailOrder, name='detail-order'),
    path('asasdsadsadsadasda', views.mail, name='mail'),
]
