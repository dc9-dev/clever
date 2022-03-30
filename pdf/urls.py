from django.urls import path
from . import views

urlpatterns = [

    # path('', views.search_form),
    path('getpdf/<int:id>', views.generate_pdf, name='getpdf'),
    path('getpdf/cash/<int:id>/<str:date>', views.GenereatePdfRaport.as_view(), name='cash-report'),
    path('getpdf/offer/<int:id>', views.GeneratePdfOffer.as_view(), name='offer-pdf'),
]
