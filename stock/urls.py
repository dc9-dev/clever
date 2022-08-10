from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views


urlpatterns = [
    path('stocks/', staff_member_required(views.StockView.as_view()), name='stocks'),
    path('', views.WarehouseListView.as_view(), name='home-stock'),
    path('new/', staff_member_required(views.CreateStock.as_view()), name='create-stock'),
    path('add/<int:id>', views.AddStock, name='add-stock'),
    path('stocks/delete/<int:id>', views.DeleteStock, name='delete-stock'),
    path('take/<int:id1>/<int:id2>', views.TakeStock, name='take-stock'),
    path('grn/', views.GRN, name='grn'),
    path('grn/edit/<int:id>', views.EditGRN, name='edit-grn'),
    path('grn/detail/<int:id>', views.DetailGRN, name='detail-grn'),
    path('material/create/', views.MaterialCreateView.as_view(), name='create-material'),
    path('services/create/', views.ServicesCreateView.as_view(), name='create-services'),
    path('contractor', views.ContractorCreateView.as_view(), name='create-contractor'),
    path('contractor/edit/', views.ContractorUpdateView.as_view(), name='edit-contractor'),
    path('getpdf/<int:id>', views.Generate_stock_label_not_production, name='label-pdf'),

]
