import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class StockFilter(django_filters.FilterSet):
    

    class Meta:
        model = Stock
        fields = {
            'length': ['gte'],
            'width': ['gte'],
            'material': ['exact'],
        }
