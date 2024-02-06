# your_project/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from flogi import consumers  # Import your WebSocket consumer

websocket_urlpatterns = [
    path('ws/some_path/', consumers.MyConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
    # (http->django views is added by default)
})
