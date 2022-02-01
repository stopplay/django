from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False, default="myemai@email.com")
    address = models.ForeignKey('users.Address', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=('User Address'))


class Establishement(models.Model):
    establishement_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False, default="myemai@email.com")
    address = models.ForeignKey('users.Address', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=('Establishment Address'))


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_line_1 =  models.TextField(null=True, blank=True)
    address_line_2 = models.TextField(null=True, blank=True)
    town =  models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    post_code = models.TextField(null=True, blank=True)

