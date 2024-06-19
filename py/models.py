from django.db import models
from django.conf import settings
from django.apps import apps

settings.configure()
# hi this is liz
if not apps.ready:
    apps.populate(settings.INSTALLED_APPS)

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    class Meta:
        app_label = 'employee_app'

class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    class Meta:
        app_label = 'department_app'