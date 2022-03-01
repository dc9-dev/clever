from django import forms
from .models import (Production,
                     ProductionMaterial,
                     ProductionComments,
                     ProductionOrder)
from order.models import Material


class ProductionMaterialForm(forms.ModelForm):

    area = forms.DecimalField(required=True)

    class Meta:
        model = ProductionMaterial
        exclude = ['production']


class ProductionCommentsForm(forms.ModelForm):

    class Meta:
        model = ProductionComments
        fields = ['comment']


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = ProductionOrder
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EditOrderForm(forms.ModelForm):

    class Meta:
        model = ProductionOrder
        exclude = ['customer', 'date', 'order']
