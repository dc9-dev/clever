from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views


urlpatterns = [
    path('', staff_member_required(views.StockView.as_view()), name='stock'),
    path('new/', staff_member_required(views.CreateStock.as_view()), name='create-stock'),
    path('add/<int:id>', views.AddStock, name='add-stock'),
    path('take/<int:id1>/<int:id2>', views.TakeStock, name='take-stock'),
    path('cutter/sharp/<int:id>', views.CutterSharp, name='cutter-sharp'),
    path('grn/', views.GRN, name='grn'),
    path('grn/edit/<int:id>', views.EditGRN, name='edit-grn'),
    path('grn/detail/<int:id>', views.DetailGRN, name='detail-grn'),
    path('production/', views.ProductionHome, name='home-production'),
    path('production/new/', views.CreateProduction, name='create-production'),
    path('production/<int:id>/edit', views.EditProduction, name='edit-production'),
    path('production/<int:id>/detail', views.DetailProduction, name='detail-production'),
    path('production/<int:id>/filter', views.ProductionStockFilter, name='production-filter'),
    path('production/<int:id>/stockin', views.ProductionStockIn, name='stockin'),
    path('production/comments/<int:id>', views.ProductionComments, name='comments'),
    path('production/status/<int:id>', views.ProductionStatus, name='status'),
   # path('production/raport', views.ProductionRaport, name='raport-production'),
]