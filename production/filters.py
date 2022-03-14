from django.conf import settings
import django_filters 
from django_filters import ModelChoiceFilter, CharFilter, DateFilter
from .models import *

class ProductionOrderFilter(django_filters.FilterSet):
    customer = ModelChoiceFilter(label='Klient', queryset=Customer.objects.all())
    order = CharFilter(field_name='order', label='Zamówienie nr', lookup_expr='icontains')
    date_start = DateFilter(
        field_name='date', 
        label='Data od:',
        input_formats=settings.DATE_INPUT_FORMATS,
        lookup_expr='gte'
        )
    date_end = DateFilter(
        field_name='date', 
        label='Data do:',
        input_formats=settings.DATE_INPUT_FORMATS,
        lookup_expr='lte'
        )

    class Meta:
        model = ProductionOrder
        exclude = ['date']
