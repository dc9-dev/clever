import django_filters
from django_filters import CharFilter

from .models import Customer
from stock.models import Contractor


class CustomerFilter(django_filters.FilterSet):
    company = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['company']


class ContractorFilter(django_filters.FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Contractor
        fields = ['name']