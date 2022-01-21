from django import forms
from order.models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('order',)
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control task'
          