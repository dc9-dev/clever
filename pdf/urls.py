from django.urls import path
from . import views

urlpatterns = [

    # path('', views.search_form),
    path('getpdf/<int:id>', views.generate_pdf, name='getpdf'),
    path('getpdf/cash/<int:id>/<str:date>', views.GenereatePdfRaport.as_view(), name='cash-report'),
]
