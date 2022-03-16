from django import forms
from stock.models import Stock, GoodsReceivedNote, GRNMaterial, Contractor, Payment
from order.models import Material
from production.models import Services

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

    class Meta:
        model = GRNMaterial
        exclude = ['grn', 'price_net', 'price_gross', 'vat_amount']

class CreateMaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateMaterialForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Material
        fields = '__all__'

class CreateServicesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateServicesForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Services
        fields = '__all__'

class CreateContractorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateContractorForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Contractor
        fields = '__all__'

class CreatePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePaymentForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        exclude = ['status']