from django import forms
from core.models import CampaignVolunteer, Volunteer

class CampaignVolunteerForm(forms.ModelForm):
    class Meta:
        model = CampaignVolunteer
        fields = ['volunteer']
        widgets = {
            'volunteer': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        campaign = kwargs.pop('campaign', None)
        super().__init__(*args, **kwargs)
        if campaign:
            used = campaign.campaign_volunteers.values_list('volunteer_id', flat=True)
            self.fields['volunteer'].queryset = Volunteer.objects.exclude(id__in=used)
