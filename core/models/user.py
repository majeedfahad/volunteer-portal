from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    SUPER_ADMIN = 'super_admin', 'Super Admin'
    CAMPAIGN_MANAGER = 'campaign_manager', 'Campaign Manager'
    DEPT_MANAGER = 'dept_manager', 'Department Manager'
    CAMPAIGN_SECTION_LEADER = 'campaign_section_leader', 'Campaign Section Leader'

class User(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.DEPT_MANAGER
    )

    def __str__(self):
        return self.get_full_name() or self.username
