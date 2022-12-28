from django.contrib.auth.models import User
from rest_framework import serializers


from users.models import Address, Establishment, User, Order, Settings


class SettingSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Settings
        fields = ['name', 'websocket']

class AddressSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line_1', 'address_line_2', 'town', 'city', 'post_code']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'establishment', 'comment', 'stuart_delivery_size']

class UserSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'phone', 'email', 'address']

class EstablishmentSerielizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Establishment
        fields = ['id', 'companyname', 'name','surname','email', 'phone','address']