from rest_framework import serializers
from .models import Segment, Video, SegmentImage


class SegmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SegmentImage
        fields = ['image_url']

class SegmentSerializer(serializers.ModelSerializer):
    image = SegmentImageSerializer(read_only=True)  # Reverse lookup for one-to-one relation

    class Meta:
        model = Segment
        fields = ['segment_key', 'user', 'title', 'context', 'segment_text', 'created_at', 'image']

class VideoSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True, read_only=True)  # Reverse lookup for many-to-many relation

    class Meta:
        model = Video
        fields = ['id', 'title', 'video_url', 'segments','style']
