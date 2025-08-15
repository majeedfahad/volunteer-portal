from django.db import models
from django.core.exceptions import ValidationError
from core.models import CampaignVolunteer, CampaignSection

class SectionAssignment(models.Model):
    campaign_volunteer = models.ForeignKey(
        CampaignVolunteer, on_delete=models.CASCADE,
        related_name='section_assignments'
    )
    campaign_section = models.ForeignKey(
        CampaignSection, on_delete=models.CASCADE,
        related_name='assignments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('campaign_volunteer', 'campaign_section')

    def clean(self):
        # تأكد إن نفس الحملة
        if self.campaign_volunteer.campaign_id != self.campaign_section.campaign_id:
            raise ValidationError("Volunteer and Section must belong to the same campaign.")

        # احترم max_volunteers
        current_count = self.campaign_section.assignments.count()
        if not self.pk and self.campaign_section.max_volunteers and current_count >= self.campaign_section.max_volunteers:
            raise ValidationError("This section reached its maximum number of volunteers.")

        # (اختياري) تمنع المتطوع أن يُسند لأكثر من ركن في نفس الحملة:
        already_in_campaign = SectionAssignment.objects.filter(
            campaign_volunteer=self.campaign_volunteer,
            campaign_section__campaign=self.campaign_section.campaign
        )
        if not self.pk and already_in_campaign.exists():
            raise ValidationError("This volunteer is already assigned to a section in this campaign.")

    def __str__(self):
        return f"{self.campaign_volunteer.volunteer.name} → {self.campaign_section.section.name}"
