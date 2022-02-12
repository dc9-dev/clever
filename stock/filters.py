import django_filters
from django_filters import NumberFilter

from .models import *

class StockFilter(django_filters.FilterSet):
    length = NumberFilter(lookup_expr='gte')
    width = NumberFilter(lookup_expr='gte')

    class Meta:
        model = Stock
        exclude = ['warehouse']

