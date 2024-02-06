from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import *
from .constants import *


def send_g(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "group.message",  # Your consumer should handle this type
            "message": message,
        }
    )

def send_c(channel_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "consumer.message",  # Your consumer should handle this type
            "message": message,
        }
    )

def send_s(serializer_class, instance):
    serializer = serializer_class(instance)
    if serializer.is_valid():
        return serializer.data
    return {}