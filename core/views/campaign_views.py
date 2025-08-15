from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from core.forms.campaign_form import CampaignForm
from core.forms.campaign_section_form import CampaignSectionForm
from core.forms.campaign_volunteer_form import CampaignVolunteerForm
from core.forms.section_assignment_form import SectionAssignmentForm
from core.models import Campaign, SectionAssignment


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

    # نماذج بيانات الحملة + إضافة ركن + إضافة متطوع للحملة
    form = CampaignForm(request.POST or None, instance=campaign)
    section_form = CampaignSectionForm(request.POST or None, campaign=campaign, prefix='sec')
    volunteer_form = CampaignVolunteerForm(request.POST or None, campaign=campaign, prefix='vol')

    # الأركان المرتبطة بالحملة مع عدّاد المعيّنين
    sections_qs = campaign.campaign_sections.select_related('section').annotate(
        current_count=Count('assignments')
    )
    sections = list(sections_qs)

    # جهّز لكل ركن:
    # - قائمة المعيّنين (assigned_list)
    # - فورم إسناد خاص، instance فيه campaign_section مضبوط مسبقًا
    for s in sections:
        s.assigned_list = s.assignments.select_related('campaign_volunteer__volunteer')
        s.assign_form = SectionAssignmentForm(
            request.POST or None,
            campaign=campaign,
            prefix=f'assign_{s.id}',
            instance=SectionAssignment(campaign_section=s),
        )

    if request.method == 'POST':
        # حفظ بيانات الحملة
        if 'save_campaign' in request.POST and form.is_valid():
            form.save()
            messages.success(request, 'Campaign saved.')
            return redirect('campaign-edit', campaign_id=campaign.id)

        # ربط ركن جديد بالحملة
        if 'add_section' in request.POST and section_form.is_valid():
            cs = section_form.save(commit=False)
            cs.campaign = campaign
            try:
                cs.save()
                messages.success(request, 'Section linked to campaign.')
            except IntegrityError:
                messages.error(request, 'Section already linked.')
            return redirect('campaign-edit', campaign_id=campaign.id)

        # إضافة متطوع جديد للحملة
        if 'add_volunteer' in request.POST and volunteer_form.is_valid():
            cv = volunteer_form.save(commit=False)
            cv.campaign = campaign
            try:
                cv.save()
                messages.success(request, 'Volunteer added to campaign.')
            except IntegrityError:
                messages.error(request, 'Volunteer already in campaign.')
            return redirect('campaign-edit', campaign_id=campaign.id)

        # إسناد متطوع لركن محدد (نحدده من زر الإرسال)
        for cs in sections:
            btn_name = f'add_assignment_{cs.id}'
            if btn_name in request.POST:
                form_assign = cs.assign_form  # instance يحتوي campaign_section مُسبقًا
                if form_assign.is_valid():
                    assignment = form_assign.save(commit=False)  # فيه campaign_volunteer من الفورم
                    try:
                        assignment.full_clean()  # يتأكد: نفس الحملة + عدم تجاوز max + عدم التكرار + متطوع واحد لكل حملة
                        assignment.save()
                        messages.success(request, f'Volunteer assigned to "{cs.section.name}".')
                    except ValidationError as e:
                        messages.error(request, '; '.join(sum(e.message_dict.values(), [])))
                    except IntegrityError:
                        messages.error(request, 'This assignment already exists.')
                else:
                    messages.error(request, 'Please select a volunteer.')
                return redirect('campaign-edit', campaign_id=campaign.id)

    # متطوعو الحملة (للعمود الأيمن)
    volunteers = campaign.campaign_volunteers.select_related('volunteer').all()

    return render(request, 'campaigns/edit.html', {
        'campaign': campaign,
        'form': form,
        'section_form': section_form,
        'volunteer_form': volunteer_form,
        'sections': sections,   # تحتوي current_count + assigned_list + assign_form
        'volunteers': volunteers,
    })
