from urllib import response
from drf_yasg.utils import swagger_auto_schema, no_body
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from users import services
from users.admin import EstablishmentAdmin
from users.models import User, Establishment, Address, Order
from users.serializer import UserSerielizer, EstablishmentSerielizer, AddressSerielizer, OrderSerializer
from users.services import validate_user_address ,validate_establishments_address, post_stuart_price, post_stuart_job
from rest_framework.decorators import action
from django.http import HttpResponse, Http404, HttpResponseRedirect


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerielizer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True)
    def validate_an_address(self, request, pk):
        # //get the objects from the ViewSet
        user = self.get_object()
        # //serialize the objects from they ViewSet
        serializer = UserSerielizer(user, context={'request': request})
        # the data needs to send to the service the object
        data = validate_user_address(user)
        return Response(data, content_type="application/json")


class EstablishmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Establishments to be viewed or edited.
    """
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerielizer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True)
    def validate_an_address(self, request, pk):
        establishement = self.get_object()
        serializer = EstablishmentSerielizer(establishement, context={'request': request})
        data = validate_establishments_address(establishement)
        return Response(data, content_type="application/json")


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=True)
    def request_stuart_price(self, request, pk):
        order = self.get_object()
        print(order)
        serializer = OrderSerializer(order, context={'request': request})
        data = post_stuart_price(order)
        return Response(data, status=200,content_type="application/json")

    @action(methods=['get'], detail=True)
    def request_stuart_job(self, request, pk):
        order = self.get_object()
        print(order)
        serializer = OrderSerializer(order, context={'request': request})
        data = post_stuart_job(order)
        return Response(data, status=200,content_type="application/json")


class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint Address.
    """     
    queryset = Address.objects.all().order_by('-id')
    serializer_class = AddressSerielizer
    permission_classes = [permissions.IsAuthenticated]

