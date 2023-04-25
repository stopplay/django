from django.urls import path
from . import consumers
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import routing


websocket_urlpatterns = [
    path('ws/scan_qr_code/<str:qr_code_data>/', consumers.QRCodeConsumer.as_asgi()),
]
