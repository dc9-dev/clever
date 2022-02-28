from django import forms
from stock.models import Stock, GoodsReceivedNote, GRNMaterial
from order.models import Material

#  Production, ProductionMaterial, ProductionComments,

class StockCreateForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = '__all__'


# class ProductionMaterialForm(forms.ModelForm):

#     area = forms.DecimalField(required=True)

#     class Meta:
#         model = ProductionMaterial
#         exclude = ['production']


# class StockCreateInForm(forms.ModelForm):
    
#     class Meta:
#         model = Stock
#         exclude = ['material']


# class ProductionCommentsForm(forms.ModelForm):

#     class Meta:
#         model = ProductionComments
#         fields = ['comment',]


class grnCreateForm(forms.ModelForm):

    class Meta:
        model = GoodsReceivedNote
        fields = ('documentID', 'contractor')

    def __init__(self, *args, **kwargs):
        super(grnCreateForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # def save(self, commit=True):
      
    #     self.instance.material.quantity += int(self.cleaned_data['quantity'])
    #     self.instance.material.save()

    #     return super(grnForm, self).save(commit=commit)


#

class GRNMaterailForm(forms.ModelForm):
   # area = forms.CharField(max_length=30)

    class Meta:
        model = GRNMaterial
        exclude = ['grn']