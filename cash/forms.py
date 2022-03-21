from django import forms
from .models import Payment


class CreatePaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePaymentForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Payment
        fields = '__all__'
