import django_filters
from django_filters import NumberFilter, ModelChoiceFilter, DateFilter, CharFilter

from .models import *


class StockFilter(django_filters.FilterSet):
    length = NumberFilter(lookup_expr='gte')
    width = NumberFilter(lookup_expr='gte')

    class Meta:
        model = Stock
        exclude = ['warehouse']


class GrnFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', label='Nr PZtki', lookup_expr='icontains')
    contractor = ModelChoiceFilter(label="Kontrahent",
                                  queryset=Contractor.objects.all(),
                                  )
    documentID = CharFilter(field_name='documentID', label='Nr dokumentu', lookup_expr='icontains')
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
        model = GoodsReceivedNote
        exclude = ['user']


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