from typing import Any
from django import forms
from django.forms.widgets import ClearableFileInput, CheckboxInput
from .models import Lister
from property.models import Property, PropertyImage


class CustomClearableFileInput(ClearableFileInput):
    template_name = 'custom_clearable_file_input.html'
    initial_text = 'View Current Image'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "is_initial": self.is_initial(value),
                "input_text": self.input_text,
                "initial_text": self.initial_text,
            }
        )
        context["widget"]["attrs"].setdefault("disabled", False)
        return context


class CustomCheckBoxInput(CheckboxInput):
    template_name = 'custom_checkbox_input.html'


class CustomImageField(forms.ImageField):
    widget = CustomClearableFileInput(
        attrs={'class': 'form-control input-file-custom'})

    def __init__(self, *args, **kwargs):
        self.existing_file = kwargs.pop('existing_file', None)
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Check if an existing file exists and render it with ClearableFileInput
        if self.existing_file:
            return self.widget.render(name, self.existing_file, attrs=attrs)
        return super().render(name, value, attrs=attrs, renderer=renderer)


class PropertyImageForm(forms.ModelForm):
    upload = CustomImageField(required=False)  # Use the custom field

    class Meta:
        model = PropertyImage
        fields = ['upload']

    def __init__(self, *args, **kwargs):
        existing_file = kwargs.pop('existing_file', None)
        super().__init__(*args, **kwargs)
        self.fields['upload'].existing_file = existing_file

    def clean(self):
        cleaned_data = super().clean()
        is_marked_for_deletion = cleaned_data.get('DELETE', False)

        # If the image is marked for deletion, clear the 'upload' field
        if is_marked_for_deletion:
            cleaned_data['upload'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        is_marked_for_deletion = self.cleaned_data.get('DELETE', False)

        if is_marked_for_deletion:
            # Delete the corresponding database record
            instance.delete()

        instance.save()

        return instance


class BasePIFormSet(forms.BaseInlineFormSet):
    def get_deletion_widget(self):
        return CustomCheckBoxInput
    # pass


PropertyImageFormSet = forms.inlineformset_factory(Property, PropertyImage, form=PropertyImageForm, formset=BasePIFormSet, can_delete=True, extra=1, max_num=6, widgets={
    'upload': forms.FileInput(attrs={'class': 'form-control'})
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
        help_texts = {
            'min_rent_duration': 'Please enter the value in months. (Num of years x 12, e.g 2 years = 2 x 12 = 24)',
            'max_rent_duration': 'Please enter the value in months. (Num of years x 12, e.g 2 years = 2 x 12 = 24)',
        }
        labels = {
            'is_published': 'List this property as published?'
        }
