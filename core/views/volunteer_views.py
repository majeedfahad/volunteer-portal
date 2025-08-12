from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from core.forms.volunteer_form import VolunteerForm
from core.models import Volunteer

def is_super_admin(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, 'role', '') == 'super_admin')

@login_required
def index(request):
    q = request.GET.get('q')
    volunteers = Volunteer.objects.all()
    if q:
        volunteers = volunteers.filter(name__icontains=q) | volunteers.filter(phone__icontains=q)
    return render(request, 'volunteers/index.html', {'volunteers': volunteers, 'q': q})

@login_required
@user_passes_test(is_super_admin)
def create(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            v = form.save(commit=False)
            v.created_by = request.user
            v.save()
            return redirect('volunteer-show', volunteer_id=v.id)
    else:
        form = VolunteerForm()
    return render(request, 'volunteers/create.html', {'form': form})

@login_required
def show(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    return render(request, 'volunteers/show.html', {'volunteer': volunteer})

@login_required
@user_passes_test(is_super_admin)
def edit(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect('volunteer-show', volunteer_id=volunteer.id)
    else:
        form = VolunteerForm(instance=volunteer)
    return render(request, 'volunteers/edit.html', {'form': form, 'volunteer': volunteer})

@login_required
@user_passes_test(is_super_admin)
def delete(request, volunteer_id):
    volunteer = get_object_or_404(Volunteer, id=volunteer_id)
    if request.method == 'POST':
        volunteer.delete()
        return redirect('volunteer-index')
    return render(request, 'volunteers/delete_confirm.html', {'volunteer': volunteer})
