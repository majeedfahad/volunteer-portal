from django.db import models
from core.models import Section, Volunteer

class Campaign(models.Model):
    name = models.CharField(max_length=100)
    campaign_start_date = models.DateField()
    campaign_end_date = models.DateField()
    exhibition_start_date = models.DateField(null=True, blank=True)
    exhibition_end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def clean(self):
        # اختياري: تحقق ترتيب التواريخ
        from django.core.exceptions import ValidationError
        if self.campaign_end_date and self.campaign_start_date and self.campaign_end_date < self.campaign_start_date:
            raise ValidationError("campaign_end_date must be after campaign_start_date")
        if self.exhibition_start_date and self.exhibition_end_date:
            if self.exhibition_end_date < self.exhibition_start_date:
                raise ValidationError("exhibition_end_date must be after exhibition_start_date")


class CampaignSection(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_sections')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_campaigns')
    min_volunteers = models.IntegerField(default=0)
    max_volunteers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('campaign', 'section')

    def __str__(self):
        return f'{self.campaign.name} — {self.section.name}'


class CampaignVolunteer(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_volunteers')
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='volunteer_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('campaign', 'volunteer')

    def __str__(self):
        return f'{self.volunteer.name} @ {self.campaign.name}'
