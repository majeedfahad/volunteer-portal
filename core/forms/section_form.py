from django import forms
from core.models import Section

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Section name'}),
        }
