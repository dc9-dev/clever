from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeOffer.as_view(), name='home-offer'),
    path('create/', views.CreateOfferView.as_view(), name='create-offer'),
    path('edit/<int:id>', views.edit_offer, name='edit-offer'),
    path('detail/<int:pk>', views.OfferDetailView.as_view(), name='detail-offer'),
] 