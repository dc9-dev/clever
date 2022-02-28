from django import forms
from .models import Production, ProductionMaterial, ProductionComments
from order.models import Material


class ProductionMaterialForm(forms.ModelForm):

    area = forms.DecimalField(required=True)

    class Meta:
        model = ProductionMaterial
        exclude = ['production']


class ProductionCommentsForm(forms.ModelForm):

    class Meta:
        model = ProductionComments
        fields = ['comment',]
