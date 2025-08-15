from django import forms
from core.models import SectionAssignment, CampaignVolunteer

class SectionAssignmentForm(forms.ModelForm):
    class Meta:
        model = SectionAssignment
        fields = ['campaign_volunteer']
        widgets = {
            'campaign_volunteer': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        campaign = kwargs.pop('campaign', None)
        super().__init__(*args, **kwargs)
        if campaign:
            # كل متطوعي الحملة
            cvs = CampaignVolunteer.objects.filter(campaign=campaign)

            # المتطوعون الذين لديهم إسناد لأي ركن داخل هذه الحملة (نستبعدهم)
            assigned_cv_ids = SectionAssignment.objects.filter(
                campaign_section__campaign=campaign
            ).values_list('campaign_volunteer_id', flat=True)

            self.fields['campaign_volunteer'].queryset = (
                cvs.exclude(id__in=assigned_cv_ids)
                   .select_related('volunteer')
                   .order_by('volunteer__name')
            )
            # (اختياري) تحسين عرض الاسم في القائمة
            self.fields['campaign_volunteer'].label_from_instance = (
                lambda cv: f'{cv.volunteer.name} — {cv.volunteer.phone}'
            )
