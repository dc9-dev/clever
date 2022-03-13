import django_filters 

from .models import *

class ProductionOrderFilter(django_filters.FilterSet):
    class Meta:
        model = ProductionOrder
        fields = '__all__'