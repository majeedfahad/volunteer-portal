from django.urls import path
from core.views import dashboard_views

urlpatterns = [
    path('', dashboard_views.index, name='dashboard'),
]
