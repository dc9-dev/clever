from django.views.generic import ListView
from django.shortcuts import render

from .filters import StockFilter
from .models import Stock, Material, Production


class Stock(ListView):
    model = Stock
    template_name = 'stock/home.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET, queryset=self.get_queryset()),
            'materials': Material.objects.all().order_by('name'),
            'productioins': Production.objects.all().order_by('-date'),
            })
        return context