from django import forms
from core.models import Department, User

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'manager']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
        }
