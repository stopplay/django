from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from users.serializer import UserSerielizer, EstablishmentSerielizer, AddressSerielizer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerielizer
    permission_classes = [permissions.IsAuthenticated]

class EstablishmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Establishments to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = EstablishmentSerielizer
    permission_classes = [permissions.IsAuthenticated]


class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint Address.
    """     
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AddressSerielizer
    permission_classes = [permissions.IsAuthenticated]
    



