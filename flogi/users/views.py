from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView 
from rest_framework import generics
from rest_framework.response import Response
import datetime
from dateutil import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
import openai
from users.serializers import UserSerializer
from users.models import User 
import jwt
import datetime


class RegisterView(APIView):

    @action(detail=True, methods=['post'])
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):

    @action(detail=True, methods=['post'])
    def post(self, request): 
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        payload = {
            'id' : user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)


        response.data (
            {
                "token" : token
            }
        )

        return response

class UserView(APIView):

    @action(detail=True, methods=['get'])
    def get(self, request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated Session')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except:
            raise AuthenticationFailed('Unauthenticated Session')

        user = User.objects.filter(payload['id']).first()
        
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    
    @action(detail=True, methods=['post'])
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message' : 'Logged Out'
        }
        return response


