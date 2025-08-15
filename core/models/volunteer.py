# core/models/volunteer.py
from django.db import models
from core.models import User

class VolunteerGender(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=VolunteerGender.choices)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_volunteers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} ({self.phone})'
