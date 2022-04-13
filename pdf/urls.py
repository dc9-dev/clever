from django.urls import path
from . import views

urlpatterns = [
    path('getpdf/<int:id>', views.GenerateOrderPdf.as_view(), name='getpdf'),
    path('getpdf/cash/<int:id>/<str:date>', views.GenereatePdfRaport.as_view(), name='cash-report'),
    path('getpdf/offer/<int:id>', views.GeneratePdfOffer.as_view(), name='offer-pdf'),
    #path('getpdf/stocks/<str:material>', views.)\
    path('getstockpdf/<int:id>', views.generate_stock_label, name='label'),
    path('getpdf/production/<int:id>', views.GenerateProductionPdf.as_view(), name='label-production'),
]
