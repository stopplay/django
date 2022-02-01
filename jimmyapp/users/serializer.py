from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Address, Establishment, User

class UserSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name','email', 'address']


class EstablishmentSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Establishment
        fields = ['establishment_id', 'name','email', 'address']



class AddressSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['address_id', 'address_line_1', 'address_line_2', 'town', 'city', 'post_code']