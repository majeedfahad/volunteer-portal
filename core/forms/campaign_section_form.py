from django import forms
from core.models import CampaignSection, Section

class CampaignSectionForm(forms.ModelForm):
    class Meta:
        model = CampaignSection
        fields = ['section', 'min_volunteers', 'max_volunteers']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-select'}),
            'min_volunteers': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'max_volunteers': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        campaign = kwargs.pop('campaign', None)
        super().__init__(*args, **kwargs)
        # (اختياري) استبعد الأقسام المضافة مسبقًا لهذه الحملة
        if campaign:
            used_ids = campaign.campaign_sections.values_list('section_id', flat=True)
            self.fields['section'].queryset = Section.objects.exclude(id__in=used_ids)
