from django.urls import path
from core.views import volunteer_views

urlpatterns = [
    path('', volunteer_views.index, name='volunteer-index'),
    path('create/', volunteer_views.create, name='volunteer-create'),
    path('<int:volunteer_id>/', volunteer_views.show, name='volunteer-show'),
    path('<int:volunteer_id>/edit/', volunteer_views.edit, name='volunteer-edit'),
    path('<int:volunteer_id>/delete/', volunteer_views.delete, name='volunteer-delete'),
]
