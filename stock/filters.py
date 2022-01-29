import django_filters
from django_filters import DateFilter, CharFilter

from order.models import Material
from .models import *

class StockFilter(django_filters.FilterSet):

    class Meta:
        model = Stock
        fields = ('__all__') 