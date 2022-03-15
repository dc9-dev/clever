from django import forms
from .models import UserBase, Customer

class LoginForm(forms.Form):

    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hasło'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(forms.ModelForm):

    email = forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'powtórz hasło'}))

    class Meta:
        model = UserBase
        fields = ('email', 'first_name', 'last_name')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('hasła nie są takie same')
            return cd['password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for input, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CustomerCreateForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        #fields = ['e-mail', 'firma', 'Imię', 'Naziwsko', 'Tel.', 'Kod Pocztowy', 'Adres', 'Miasto', 'Saldo'],  # sprawdz pozniej
        super(CustomerCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # for name in self.fields:
            #     visible.field.widget.attrs['placeholder'] = list(fields) # to tez
            
            
            
        