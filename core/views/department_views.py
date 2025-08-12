from django.shortcuts import render, get_object_or_404, redirect
from core.models import Department
from core.models import Section
from core.forms.department_form import DepartmentForm
from core.forms.section_form import SectionForm

def index(request):
    departments = Department.objects.all()
    return render(request, 'departments/index.html', {
        'departments': departments
    })

def show(request, department_id):
    department = get_object_or_404(Department.objects.prefetch_related('sections', 'manager'), id=department_id)
    return render(request, 'departments/show.html', {
        'department': department
    })

def create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            return redirect('department-show', department_id=department.id)
    else:
        form = DepartmentForm()

    return render(request, 'departments/create.html', {'form': form})

def edit(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    sections = Section.objects.filter(department=department)

    dept_form = DepartmentForm(request.POST or None, instance=department)
    section_form = SectionForm()

    if request.method == 'POST':
        if 'save_department' in request.POST:
            if dept_form.is_valid():
                dept_form.save()
                return redirect('department-edit', department_id=department.id)

        elif 'add_section' in request.POST:
            section_form = SectionForm(request.POST)
            if section_form.is_valid():
                section = section_form.save(commit=False)
                section.department = department
                section.save()
                return redirect('department-edit', department_id=department.id)

    return render(request, 'departments/edit.html', {
        'form': dept_form,
        'department': department,
        'sections': sections,
        'section_form': section_form
    })
