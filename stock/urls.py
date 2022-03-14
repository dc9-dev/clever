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
    
]
