from django import forms
from .models import Payment


class CreatePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePaymentForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        exclude = ['user', 'IW_IY', 'status']


class UpdatePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdatePaymentForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        exclude = ['__all__']