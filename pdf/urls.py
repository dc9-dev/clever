from django.urls import path
from . import views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
  
    #path('', views.search_form),
    path('getpdf/', views.generate_pdf),

]
