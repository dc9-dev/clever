from django import forms
from stock.models import Stock, GoodsReceivedNote, GRNMaterial
from order.models import Material

#  Production, ProductionMaterial, ProductionComments,

class StockCreateForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = '__all__'


class StockCreateInForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        exclude = ['material']


class grnCreateForm(forms.ModelForm):

    class Meta:
        model = GoodsReceivedNote
        fields = ('documentID', 'contractor')

    def __init__(self, *args, **kwargs):
        super(grnCreateForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class GRNMaterailForm(forms.ModelForm):
   # area = forms.CharField(max_length=30)

    class Meta:
        model = GRNMaterial
        exclude = ['grn']