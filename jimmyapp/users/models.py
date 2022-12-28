from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.

class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False, default="Provider")
    websocket = models.TextField(null=True, blank=True, default="WebsocketURL")

    def __str__(self):
        if self.websocket:
            return f'{self.websocket}'
        return ''   

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False, default="Name")
    surname = models.CharField(max_length=255, null=False, blank=False, default="Surname")
    phone = models.CharField(max_length=100, null=False, blank=False, default="07890655555")
    email = models.EmailField(max_length=100, null=False, blank=False, default="myemai@email.com")
    address = models.ForeignKey('users.Address', blank=True, null=True, on_delete=models.SET_NULL, related_name=('address'))

    def __str__(self):
        if self.name:
            return f'{self.name}'
        return '' 
        

class Establishment(models.Model):
    id = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=255, null=False, blank=False, default="Company Name")
    name = models.CharField(max_length=255, null=False, blank=False, default="Name")
    surname = models.CharField(max_length=255, null=False, blank=False, default="Surname")
    phone = models.CharField(max_length=100, null=False, blank=False, default="07890655555")
    email = models.EmailField(max_length=100, null=False, blank=False, default="myemai@email.com")
    address = models.ForeignKey('users.Address', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=('Establishment Address'))

    def __str__(self):
        if self.companyname:
            return f'{self.companyname}, {self.address} '
        return ''   

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address_line_1 =  models.TextField(null=True, blank=True)
    address_line_2 = models.TextField(null=True, blank=True)
    town =  models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    post_code = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.address_line_1:
            return f'{self.address_line_1},{self.address_line_2},{self.post_code}'
        return ''

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    SIZE_CHOICES = [('Small', 'Small'),('Medium', 'Medium')]
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(null=True, blank=True)
    stuart_delivery_fee = models.FloatField(null=True, blank=True)
    user = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=('Order User'))
    establishment = models.ForeignKey('users.Establishment', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=('Order Establishment'))
    comment = models.TextField(null=True, blank=True)
    STUART_DELIVERY_SIZE_CHOICES = [('Small', 'Small'),('Medium', 'Medium'), ('Large' , 'Large')]
    stuart_delivery_size = models.CharField(max_length=50, choices=STUART_DELIVERY_SIZE_CHOICES)
    stuart_delivery_id = models.IntegerField(null=True, blank=True)
    stuart_tracking_url =  models.TextField(null=True, blank=True)
    stuart_delivery_status =  models.TextField(null=True, blank=True)
    stuart_pickup = models.DateTimeField(null=True, blank=True)
    stuart_delivery_distance = models.FloatField(null=True, blank=True)
    stuart_delivery_duration = models.FloatField(null=True, blank=True)


    def __str__(self):
        if self.number:
            return f'Order number: {self.number}, client : {self.user}, establishment: {self.establishment}'
        return ''

    def pricing(self):
        if self.stuart_delivery_fee:
            return f'{self.stuart_delivery_fee}'
        return ''

