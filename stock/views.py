from django.views import View
from django.views.generic import ListView

from .filters import StockFilter
from .models import Stock


class Stock(ListView):
    model = Stock
    template_name = 'stock/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = StockFilter(self.request.GET, queryset=self.get_queryset())
        return context