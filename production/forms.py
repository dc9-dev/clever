from django import forms
from stock.models import Material, Gender

from account.models import Customer
from .models import (Attachment,
                     ProductionMaterial,
                     ProductionComments,
                     ProductionOrder,
                     MaterialServices,
                     Comment,)


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
    customer = forms.ModelChoiceField(Customer.objects.order_by('company'))
    class Meta:
        model = ProductionOrder
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class EditOrderForm(forms.ModelForm):

    class Meta:
        model = MaterialServices
        exclude = ['productionorder', 'total_price']
        
    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.none()
        
        if 'gender' in self.data:
            print("elo from form")
            try:
                gender_id = int(self.data.get('gender'))
                self.fields['material'].queryset = Material.objects.filter(gender_id=gender_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['material'].queryset = self.instance.Material.material_set.order_by('name')

class AttachmentForm(forms.ModelForm):
    file = forms.FileField(label='',)

    class Meta:
        model = Attachment
        fields = ['file']
    
    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm mt-3 ms-3'


class CommentForm(forms.ModelForm):
    content = forms.CharField(
                    label='Napisz komentarz', 
                    widget=forms.Textarea(attrs={'rows': '2',})
                    )

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm mt-3 float-start'
