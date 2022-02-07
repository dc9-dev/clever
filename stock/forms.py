from django import forms
from stock.models import Production
from order.models import Material



class ProductionForm(forms.ModelForm):
    

    class Meta:
        model = Production
        exclude= ['order', 'user', 'producion']
        widgets = {
          'comments': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

