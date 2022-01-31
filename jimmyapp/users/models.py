from django.db import models

# Create your models here.
from django.utils import timezone


class Person(models.Model):

    app_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, Blank=False)
    phone = models.CharField(max_length=15, null=False, Blank=False)
    email = models.EmailField(null=False, blank=False)