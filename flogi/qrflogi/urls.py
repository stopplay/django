from django.urls import path
from .views import generate_qr, QRCodeList, ScanEvent

urlpatterns = [
    path('generate-qr/', generate_qr, name='generate_qr'),
    path('qr-codes/', QRCodeList.as_view(), name="QR Code List"),
    path('scan-event/', ScanEvent.as_view(), name="Scan Events")
]
