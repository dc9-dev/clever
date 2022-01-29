from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views

urlpatterns = [
	#path('', views.stock, name='stock'),
	#path('search', views.stock_search, name='stock_search'),
	path('', staff_member_required(views.Stock.as_view()), name='stock'),
	#path('stock_take/<stock_id>', views.stock_take, name='stock_take'),
]