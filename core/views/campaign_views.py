from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages

from core.forms.campaign_form import CampaignForm
from core.forms.campaign_section_form import CampaignSectionForm
from core.forms.campaign_volunteer_form import CampaignVolunteerForm
from core.models import Campaign, CampaignSection, CampaignVolunteer

def is_super_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'role', '') == 'super_admin')

@login_required
def index(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaigns/index.html', {'campaigns': campaigns})

@login_required
@user_passes_test(is_super_admin)
def create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            c = form.save()
            messages.success(request, 'Campaign created.')
            return redirect('campaign-edit', campaign_id=c.id)
    else:
        form = CampaignForm()
    return render(request, 'campaigns/create.html', {'form': form})

@login_required
def show(request, campaign_id):
    campaign = get_object_or_404(
        Campaign.objects.prefetch_related('campaign_sections__section', 'campaign_volunteers__volunteer'),
        id=campaign_id
    )
    return render(request, 'campaigns/show.html', {'campaign': campaign})

@login_required
@user_passes_test(is_super_admin)
def edit(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    form = CampaignForm(request.POST or None, instance=campaign)
    section_form = CampaignSectionForm(request.POST or None, campaign=campaign, prefix='sec')
    volunteer_form = CampaignVolunteerForm(request.POST or None, campaign=campaign, prefix='vol')

    if request.method == 'POST':
        if 'save_campaign' in request.POST and form.is_valid():
            form.save()
            messages.success(request, 'Campaign saved.')
            return redirect('campaign-edit', campaign_id=campaign.id)

        elif 'add_section' in request.POST and section_form.is_valid():
            cs = section_form.save(commit=False)
            cs.campaign = campaign
            try:
                cs.save()
                messages.success(request, 'Section linked to campaign.')
            except IntegrityError:
                messages.error(request, 'Section already linked.')
            return redirect('campaign-edit', campaign_id=campaign.id)

        elif 'add_volunteer' in request.POST and volunteer_form.is_valid():
            cv = volunteer_form.save(commit=False)
            cv.campaign = campaign
            try:
                cv.save()
                messages.success(request, 'Volunteer added to campaign.')
            except IntegrityError:
                messages.error(request, 'Volunteer already in campaign.')
            return redirect('campaign-edit', campaign_id=campaign.id)

    sections = campaign.campaign_sections.select_related('section').all()
    volunteers = campaign.campaign_volunteers.select_related('volunteer').all()

    return render(request, 'campaigns/edit.html', {
        'campaign': campaign,
        'form': form,
        'section_form': section_form,
        'volunteer_form': volunteer_form,
        'sections': sections,
        'volunteers': volunteers,
    })
