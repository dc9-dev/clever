from django import forms
from stock.models import Production, Stock, ProductionMaterial
from order.models import Material


class StockCreateForm(forms.ModelForm):
    
    class Meta:
    	model = Stock
    	fields = '__all__'


class ProductionMaterialForm(forms.ModelForm):

	class Meta:
		model = ProductionMaterial
		exclude = ['production']


class StockCreateInForm(forms.ModelForm):
    
    class Meta:
    	model = Stock
    	exclude = ['material']

