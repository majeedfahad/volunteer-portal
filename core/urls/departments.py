from django.urls import path
from core.views import department_views

urlpatterns = [
    path('', department_views.index, name='department-index'),
    path('<int:department_id>/', department_views.show, name='department-show'),
    path('create/', department_views.create, name='department-create'),
    path('<int:department_id>/edit/', department_views.edit, name='department-edit'),
]
