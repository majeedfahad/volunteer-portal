from django.urls import path
from core.views import campaign_views

urlpatterns = [
    path('', campaign_views.index, name='campaign-index'),
    path('create/', campaign_views.create, name='campaign-create'),
    path('<int:campaign_id>/', campaign_views.show, name='campaign-show'),
    path('<int:campaign_id>/edit/', campaign_views.edit, name='campaign-edit'),
]
