from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from . import views

urlpatterns = [
	path('', staff_member_required(views.Stock.as_view()), name='stock'),

]