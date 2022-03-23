from django.urls import path
from . import views

urlpatterns = [
    path('', views.CashListView.as_view(), name='cashes'),
    path('detail/<int:id>', views.CashDetail, name='cash-detail'),
    path('payment/create/<int:id>', views.PaymentCreateView, name='create-payment'),
    path('payment/search', views.SearchPaymentView.as_view(), name='search-payment'),
    path('payment/detail', views.SearchPaymentView.as_view(), name='search-payment'),
    path('payment/delete/<int:id>', views.PaymentDeleteView.as_view(), name='delete-payment'),
    path('payment/update/<int:id>', views.PaymentUpdateView.as_view(), name='update-payment'),
]