from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView 
from rest_framework import mixins
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
from django.views.decorators.csrf import csrf_exempt


class RegisterView(APIView):

    @csrf_exempt
    @action(detail=True, methods=['post'])  
    def post(self, request) :
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response("")

class LoginView(APIView):

    @action(detail=True, methods=['post'])
    def post(self, request): 

        email = self.request.data.get('email', None)
        password = self.request.data.get('password', None)

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

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)


        response.data = {
                "token" : token
            }

        return response

class UserView(APIView):

    @csrf_exempt
    @action(detail=True, methods=['get'])
    def get_token(self, request, format=None):
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
    


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        if not refresh_token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        try:
            payload = jwt.decode(refresh_token, 'refresh_secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Expired refresh token, please login again.')

        # Assuming payload contains user_id
        user = User.objects.filter(payload['id']).first()
        if not user:
            raise AuthenticationFailed('Invalid payload in refresh token.')

        # Issue new access token
        new_access_token = jwt.encode(
            {
                'user_id': user,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)  # Short expiry for access token
            },
            'access_secret',  # Separate secret for access token
            algorithm='HS256'
        )

        return Response({'access_token': new_access_token})



class LogoutView(APIView):
    
    @csrf_exempt
    @action(detail=True, methods=['post'])
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message' : 'Logged Out'
        }
        return response


