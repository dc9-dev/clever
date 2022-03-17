import django_filters
from django_filters import ModelChoiceFilter, DateFilter, CharFilter

from .models import *


class PaymentFilter(django_filters.FilterSet):

    cash = ModelChoiceFilter(label="Kasa",
                                  queryset=Cash.objects.all(),
                                  )
    date = DateFilter(
        field_name='date', 
        label='Data', 
        lookup_expr='icontains', 
        input_formats=settings.DATE_INPUT_FORMATS,)
    title = CharFilter(field_name='title', label='Tytułem', lookup_expr='icontains')
    number = CharFilter(field_name='number', label='Nr', lookup_expr='icontains')
    IW_IY = CharFilter(field_name='IW_IY', label='IW_IY', lookup_expr='icontains')
    amount = CharFilter(field_name='amount', label='kwota', lookup_expr='icontains')
    
    class Meta:
        model = Payment
        exclude = ['comment', 'cash_amount']