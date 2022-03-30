from django import forms
from .models import Offer, OfferItem, Note



class CreateOfferForm(forms.ModelForm):

    class Meta:
        model = Offer
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super(CreateOfferForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OfferItemForm(forms.ModelForm):
    description = forms.CharField(
                    widget=forms.Textarea(attrs={'rows': '1',})
                )
    class Meta:
        model = OfferItem
        fields = ['description', 'quantity', 'price_net_unit', 'vat']

    def __init__(self, *args, **kwargs):
        super(OfferItemForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm'


class NoteForm(forms.ModelForm):
    content = forms.CharField(
                    label='dodaj notatkę', 
                    widget=forms.Textarea(attrs={'rows': '2',})
                    )

    class Meta:
        model = Note
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-sm mt-3 float-start'