from django import forms
from .models import Stock, GoodsReceivedNote, GRNMaterial, Contractor, Material, Gender, Comment, Attachment

from production.models import Services


# def get_tree_data():
#         def rectree(toplevel):
#             children_list_of_tuples = list()
#             for child in toplevel.objects.filter(material__grnmaterial=GRNMaterial):
#                 children_list_of_tuples.append(tuple((child.id, child.short_name)))

#             return children_list_of_tuples

#         data = list()
#         t = Gender.objects.filter()
#         for toplevel in t:
#             childrens = rectree(toplevel)
#             data.append(
#                 tuple(
#                     (
#                         toplevel.title,
#                         tuple(
#                             childrens
#                             )
#                         ) 
#                     )
#             )
#         return tuple(data)

class StockCreateForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = '__all__'
    
    def __init__(self, *args, ** kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.none()
        
        if 'gender' in self.data:
            try:
                gender_id = int(self.data.get('gender'))
                self.fields['material'].queryset = Material.objects.filter(gender_id=gender_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['material'].queryset = self.instance.Material.material_set.order_by('name')
                

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
    #material = forms.MultipleChoiceField(choices=get_tree_data())
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
