from django.conf import settings
import django_filters 
from django_filters import ModelChoiceFilter, CharFilter, DateFilter, BooleanFilter
from .models import *

class ProductionOrderFilter(django_filters.FilterSet):

    customer = ModelChoiceFilter(label='Klient', queryset=Customer.objects.all())
    order = CharFilter(field_name='order', label='Zamówienie nr', lookup_expr='icontains')
    settlement = BooleanFilter(field_name='settlement', label="Rozliczenie")
    date = DateFilter(
        field_name='date', 
        label='Data', 
        lookup_expr='icontains', 
        input_formats=settings.DATE_INPUT_FORMATS,)
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
        exclude = ['attachments']
