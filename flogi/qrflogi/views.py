from django.shortcuts import render
from flogi.settings import BASE_DIR, STATIC_ROOT, STATIC_URL, MEDIA_ROOT
import os
import qrcode
from rest_framework import generics

from .models import QRCode, ScanEvent
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import JsonResponse
from .serializers import QRCodeSerializer, ScanEventSerializer
BASE_URL = 'http://127.0.0.1:8000'

# Create your views here.s
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_qr(request):
    name = request.data.get("name", None)
    domain = request.data.get("domain", None)
    gtin = request.data.get("gtin", None)
    brand = request.data.get("brand", None)
    locale = request.data.get("locale", None)
    if domain and name:
        qr_code = QRCode.objects.create(
            domain=domain,
            gtin=gtin,
            brand=brand,
            locale=locale,
        )
    else:
        raise Exception("No domain provided")
    qr_big = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr_big.add_data(f'{domain}{name}{gtin}{brand}{locale}')
    qr_big.make()  
    img_qr_big = qr_big.make_image(fill_color="black", back_color="white")
    image_file = BytesIO()
    img_qr_big.save(image_file, 'png')
    image_file.seek(0)
    image_name = f'{name}.png'
    image_content = ContentFile(image_file.read())
    default_storage.save(f'{image_name}', image_content)
    
    link = f'{STATIC_URL}img/{image_name}'
    return JsonResponse({'link': link})

class QRCodeList(generics.ListAPIView):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

class ScanEvent(generics.ListAPIView):
    queryset = ScanEvent.objects.all()
    serializer_class = ScanEventSerializer