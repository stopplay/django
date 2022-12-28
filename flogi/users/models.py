from django.db import models

# Create your models here.

    # pizza_price = models.FloatField(null=True, blank=True)
    # size = models.ForeignKey('product.Size', on_delete=models.SET_NULL, null=True, blank=True)

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=False)

class Billing(models.Model):
    subscriber = models.ForeignKey('users.Subscriber', on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=100)
