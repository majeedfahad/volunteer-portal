from django import forms
from core.models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'name',
            'campaign_start_date', 'campaign_end_date',
            'exhibition_start_date', 'exhibition_end_date'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'campaign_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'campaign_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'exhibition_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'exhibition_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
