from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import User

class UserSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['app_id', 'first_name', 'phone_number', 'email_address']