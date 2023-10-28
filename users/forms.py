from typing import Any
from django import forms
from .models import Lister
from property.models import Property, PropertyImage


PropertyImageFormSet = forms.inlineformset_factory(Property, PropertyImage, fields=('upload',), extra=1, max_num=6, widgets={
    'upload': forms.FileInput(attrs={'class': 'form-control', 'required': True})
})


class ListerDocumentForm(forms.ModelForm):
    class Meta:
        model = Lister
        fields = [
            'business_document']
        widgets = {
            'business_document': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf'})
        }


class PropertyForm(forms.ModelForm):
    # def clean(self) -> dict[str, Any]:
    #     print('In this clean')
    #     print(self.cleaned_data)
    #     return super().clean()

    class Meta:
        model = Property
        fields = ['name', 'location_text', 'property_types', 'price', 'for_rent', 'min_rent_duration',
                  'max_rent_duration', 'currency', 'description', 'Location', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'for_rent': forms.CheckboxInput(attrs={'id': 'for_rent'}),
            'location_text': forms.TextInput(attrs={'class': 'form-control'}),
            'property_types': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_rent_duration': forms.NumberInput(attrs={'class': 'form-control', 'id': 'min_rent_duration'}),
            'max_rent_duration': forms.NumberInput(attrs={'class': 'form-control', 'id': 'max_rent_duration'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'Location': forms.Select(attrs={'class': 'form-select'}),
        }
