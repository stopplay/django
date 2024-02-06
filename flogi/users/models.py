from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']

class Address(models.Model):
    name = models.TextField(max_length=700, blank=True, null=True)
    number = models.TextField(max_length=700, blank=True, null=True)
    first_line = models.TextField(max_length=700, blank=True, null=True)
    second_line = models.TextField(max_length=700, blank=True, null=True)
    town = models.TextField(max_length=700, blank=True, null=True)
    city = models.TextField(max_length=700, blank=True, null=True)
    state = models.TextField(max_length=700, blank=True, null=True)
    zipcode = models.TextField(max_length=700, blank=True, null=True)
    additional_info = models.TextField(max_length=700, blank=True, null=True)
    active = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user" )
    phone_number = models.CharField(max_length=20, null=True, blank=True, default='')
    addresses = models.ManyToManyField(Address, blank=True, related_name="address" )

class StoryTokens(models.Model):
    token_used = models.BigIntegerField(blank=True, null = True)
    tokens_limit = models.BigIntegerField(blank=True, null = True)
    tokens_balance = models.BigIntegerField(blank=True, null = True)

class ChatGPTProfile(models.Model):
    profile = models.ForeignKey(Profile, related_name='chatgbt_profile', on_delete=models.CASCADE)
    token_used = models.BigIntegerField(blank=True, null = True)

class StripeProfile(models.Model):
    profile = models.ForeignKey(Profile, related_name='stripe_profile', on_delete=models.CASCADE)
    network_id = models.IntegerField(null=False, blank=True)
    stripe_customer_id = models.CharField(max_length=1000, null=True, blank=True, default='')
    stripe_planproduct_id = models.CharField(max_length=1000, null=True, blank=True, default='')
    stripe_subscription_id = models.CharField(max_length=1000, null=True, blank=True, default='')
    stripe_connect = models.CharField(max_length=1000, null=True, blank=True, default='')
    stripe_pm = models.CharField(max_length=1000, null=True, blank=True, default='')
    last4 = models.CharField(max_length=4, blank=True, null=True)
    card_brand = models.CharField(max_length=20, blank=True, null=True)
    account_stripe_link = models.CharField(max_length=1000, null=True, blank=True, default='')
    stripe_login_link =  models.CharField(max_length=1000, null=True, blank=True, default=None)
    account_connect_status = models.CharField(max_length=1000, null=True, blank=True, default='')
    account_stripe_KYC_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, null=True)
