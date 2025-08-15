from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from core.models import Department, Section, Volunteer, Campaign, CampaignSection, CampaignVolunteer, SectionAssignment

@login_required
def index(request):
    # أرقام سريعة
    stats = {
        'departments': Department.objects.count(),
        'sections': Section.objects.count(),
        'volunteers': Volunteer.objects.count(),
        'campaigns': Campaign.objects.count(),
        'campaign_sections': CampaignSection.objects.count(),
        'assignments': SectionAssignment.objects.count(),
    }

    # آخر العناصر (غيّر الأعداد لو حبيت)
    recent_volunteers = Volunteer.objects.select_related('created_by')[:10]
    recent_campaigns = Campaign.objects.annotate(
        sections_count=Count('campaign_sections'),
        volunteers_count=Count('campaign_volunteers')
    )[:10]

    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'recent_volunteers': recent_volunteers,
        'recent_campaigns': recent_campaigns,
    })
