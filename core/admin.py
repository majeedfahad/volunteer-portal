from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Department
from core.models import User
from .models import Volunteer

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Department)
admin.site.register(Volunteer)
