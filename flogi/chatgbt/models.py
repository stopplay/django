from django.db import models
from users.models import * 
from django.conf import settings

class ChatGBT(models.Model):
    name = models.CharField(max_length=256, null=True)
    key = models.CharField(max_length=256, null=True)

class Segment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    context = models.TextField()
    segment_text = models.TextField()
    segment_key = models.AutoField(primary_key=True)  # Auto-incrementing key
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Segment for {self.user.username} - {self.title[:50]}"

class SegmentImage(models.Model):
    segment = models.OneToOneField(Segment, on_delete=models.CASCADE, related_name="image")
    image_url = models.URLField(max_length=1024) 

class Video(models.Model):
    title = models.CharField(max_length=256, default="Video")
    video_url = models.URLField(max_length=1024, blank=True, null=True)   
    segments = models.ManyToManyField(Segment, blank=True, related_name="videos")
    style = models.CharField(max_length=256, default="Style")
    
