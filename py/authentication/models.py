from django.db import models

class ClockInTime(models.Model):
    datetime = models.DateTimeField(auto_now=True)