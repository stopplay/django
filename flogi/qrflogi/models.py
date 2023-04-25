from django.db import models
from django.utils import timezone

# Create your models here.

class QRCode(models.Model):
    name = models.CharField(max_length=255, null=True)
    domain = models.URLField(null=True)
    source = models.CharField(max_length=255, null=True)
    brand = models.CharField(max_length=255, null=True)
    gtin = models.CharField(max_length=255, null=True)
    locale = models.CharField(max_length=255, null=True)
    pixel = models.CharField(max_length=255, null=True)
    qr_code_link = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)


class ScanEvent(models.Model):
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def scan_qr_code(request, qr_code_id, x, y):
        qr_code = QRCode.objects.get(id=qr_code_id)
        ScanEvent.objects.create(qr_code=qr_code, x=x, y=y)
        qr_code.scans += 1
        qr_code.save()
