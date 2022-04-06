import django_filters
from django_filters import NumberFilter, ModelChoiceFilter, DateFilter, CharFilter

from .models import *


class StockFilter(django_filters.FilterSet):
    length = NumberFilter(lookup_expr='gte')
    width = NumberFilter(lookup_expr='gte')
    

    class Meta:
        model = Stock
        fields = '__all__'


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
