from django import forms
from stock.models import Production, Stock
from order.models import Material


class StockCreateForm(forms.ModelForm):
    
    class Meta:
    	model = Stock
    	fields = '__all__'

class ProductionForm(forms.ModelForm):

    class Meta:
        model = Production
        exclude= ['order', 'user', 'producion']
        widgets = {
          'comments': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

