from moviepy.editor import *
import boto3
import botocore
import io
from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from dateutil import *
from rest_framework.permissions import AllowAny, IsAuthenticated
import json
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import openai

import googlemaps
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from flogi.settings import OPENAIKEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN
import json
import requests
from .models import Video, Segment, SegmentImage
from celery import shared_task
from django.shortcuts import get_object_or_404
OPENAIKEY = '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'
import re
from .consumers import *
from .utils import *
from .constants import VIDEO_UPDATE_GROUP, CONSUMER_UPDATE
# from imagine import Imagine
# from imagine.styles import GenerationsStyle
# from imagine.models import Status

# Initialize the Imagine client with your API token
# client = Imagine(token="your-api-token")


save_path = 'path/to/save/images'

def upload_to_s3(file, file_name):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3_client.upload_fileobj(
                        file, 
                        AWS_STORAGE_BUCKET_NAME, 
                        file_name
)
    return f"https://{AWS_S3_CUSTOM_DOMAIN}/{file_name}"


def download_image(url, save_path, filename):
    response = requests.get(url)
    if response.status_code == 200:
        image_path = os.path.join(save_path, filename)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    else:
        return None



@shared_task
def generate_video_moviepy(video_s):
    image_list = [segment['image']['image_url'] for segment in video_s.data['segments'] if 'image' in segment]




@shared_task
def generate_story_images(video_id):
    openai.api_key = OPENAIKEY
    video = get_object_or_404(Video, id=video_id)
    video_segments = video.segments.all()

    segment_images = []
    total_segments = len(video_segments)
    processed_segements = 0
    print(total_segments)
    processed_segments = 0
    for segment in video_segments:
        # try:
        #     segment_image = SegmentImage.object.get(segment=segment)
        # except SegmentImage.DoesNotExist:

        
        prompt = f"Create an image with the style of {video.style} based on this {segment.segment_text}"
        response = openai.Image.create(
                prompt=prompt,
                n=1,  # Assuming you want one image per segment
                size="1024x1024"  # Adjust size as needed
            )
        
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)



        # # Generate an image using the generations feature
        # response = client.generations(
        #     prompt=f'''
        #             {processed_segments}
        #     ''',
        #     style=GenerationsStyle.IMAGINE_V5,
        # )

        # # Check if the request was successful
        # if response.status == Status.OK:
        #     image = response.data
        #     image.as_file("result.png")
        # else:
        #     print(f"Status Code: {response.status.value}")





        if image_response.status_code == 200:
            image_file = io.BytesIO(image_response.content)
            title = video.title.strip()
            title = title.replace(" ", "_")
            title = re.sub(r'[^\w\s]', '', title)
            s3_file_name = f"output_images/{title}_{segment.segment_key}.png"
            uploaded_image_url = upload_to_s3(image_file, s3_file_name)

            segment_image = SegmentImage.objects.update_or_create(segment=segment, image_url=uploaded_image_url)

            segment_images.append(segment_image)
            processed_segements += 1
            message = {
                        "total": total_segments, 
                    "processed": processed_segments
                    }
            send_g(VIDEO_UPDATE_GROUP, message)
        else:
            print(f"Error generating image for segment : {response.text}")
        
    completion_message = {
        "status": "complete", 
        "total": total_segments, 
        "processed": processed_segments
        }
    send_g(VIDEO_UPDATE_GROUP, completion_message)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def flogi_ai_image_create(request):

    openai.api_key = OPENAIKEY
    response = openai.Image.create(
                        prompt="A cute baby sea otter",
                        n=2,
                        size="512x512"
                        # user = ""
                        )

    return Response(data=response, status=200)