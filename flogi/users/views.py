from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from dateutil import *
from rest_framework.permissions import AllowAny, IsAuthenticated
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import openai