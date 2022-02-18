from django import forms
from stock.models import Production, Stock, ProductionMaterial, ProductionComments
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

class ProductionCommentsForm(forms.ModelForm):

	class Meta:
		model = ProductionComments
		fields = '__all__'