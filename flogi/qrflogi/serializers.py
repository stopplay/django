from rest_framework import serializers
from .models import QRCode, ScanEvent

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'

class ScanEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanEvent
        fields = '__all__'
