# consumers.py
import json
import django
django.setup()
from channels.generic.websocket import AsyncWebsocketConsumer
from qrflogi.models import QRCode, ScanEvent

class QRCodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.qr_code_data = self.scope['url_route']['kwargs']['qr_code_data']
        self.qr_code = QRCode.objects.get(data=self.qr_code_data)
        self.scan_group_name = f'scan_{self.qr_code_data}'

        await self.channel_layer.group_add(
            self.scan_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.scan_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        x = text_data_json['x']
        y = text_data_json['y']
        scan_event = ScanEvent.objects.create(qr_code=self.qr_code, x=x, y=y)
        self.qr_code.scans += 1
        self.qr_code.save()

        await self.channel_layer.group_send(
            self.scan_group_name,
            {
                'type': 'scan_event',
                'x': x,
                'y': y,
            }
        )

    async def scan_event(self, event):
        x = event['x']
        y = event['y']

        await self.send(text_data=json.dumps({
            'x': x,
            'y': y,
        }))

class EchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)