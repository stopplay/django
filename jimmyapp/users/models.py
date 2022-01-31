from django.db import models

# Create your models here.

class User(models.Model):

    app_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    email_address = models.EmailField(null=False, blank=False)