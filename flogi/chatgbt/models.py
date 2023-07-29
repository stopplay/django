from django.db import models

# Create your models here.

class ChatGBT(models.Model):
    name = models.CharField(max_length=256, null=True)
    key = models.CharField(max_length=256, null=True)
