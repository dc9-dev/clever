from django import forms
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
