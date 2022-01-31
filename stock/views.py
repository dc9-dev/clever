from django.views import View
from django.views.generic import ListView
from django.shortcuts import render
from .filters import StockFilter
from .models import Stock, Material


class Stock(ListView):
    model = Stock
    template_name = 'stock/home.html' 

    
      

    def get_context_data(self, **kwargs,):

        # for material in Material.objects.all():
        #     area = []
        #     #total_area = sum(area)
        #     for stock in material.stocks.all():
        #         result = stock.length * stock.width / 1000000
        #         area.append(result)
        #         #total_area = sum(area)

        for material in Material.objects.all():
            total_area = 0
            print(material)
            for stock in material.stocks.all():
                result = stock.length * stock.width / 1000000
                total_area += result
                print(total_area)

        context = super().get_context_data(**kwargs)
        context.update({
            'filter': StockFilter(self.request.GET, queryset=self.get_queryset()),
            'materials': Material.objects.all(),
            'total_area': total_area,
            
            })
        return context


