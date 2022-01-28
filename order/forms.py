from django import forms
from order.models import Item, Attachment


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('order',)
        widgets = {

             'width': forms.TextInput(attrs={'style': 'width: 45px'}),
             'lenght': forms.TextInput(attrs={'style': 'width: 45px'}),
             'quantity': forms.TextInput(attrs={'style': 'width: 20px'}),
             'description': forms.Textarea(attrs={'style': 'width: 60px',
                                                  'rows': 2,
                                                  'cols': 2,}),}


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        exclude = ('order',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
