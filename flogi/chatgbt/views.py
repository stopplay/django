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
from django.shortcuts import get_object_or_404

import googlemaps
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from flogi.settings import OPENAIKEY
import json
from .models import * 
from .services import *
from .serializers import SegmentSerializer, VideoSerializer

OPENAIKEY = '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'


@api_view(['GET'])
def get_all_segments(request):
    segments = Segment.objects.all()
    serializer = SegmentSerializer(segments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_videos(request):
    segments = Video.objects.all()
    serializer = VideoSerializer(segments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def generate_video_file(request, pk):
    video = get_object_or_404(Video, id=pk)
    video_s = VideoSerializer(video)
    generate_video_moviepy(video_s)


@api_view(['GET'])
def get_flogi_video(request, pk):
    video = get_object_or_404(Video, id=pk)
    serializer = VideoSerializer(video)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_flogi_ai_modules(request):

    openai.api_key = OPENAIKEY

    response = openai.Model.list()
    
    return Response(data=response, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_generate_images_for_segments(request):
    video_id = request.data.get("video")
    video = get_object_or_404(Video, id=video_id)
    generate_story_images.delay(video_id)
    serializer = VideoSerializer(video) 
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def flogi_create_video(request):
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
def flogi_story_segments(request):
    openai.api_key = OPENAIKEY

    user = request.user
    title = request.data.get("title")
    context = request.data.get("context")
    video_id = request.data.get("video")

    video = Video.objects.get(id=int(video_id))



    print(video)

    if title is None or context is None:
        return Response(data={"error": "Please provide 'title' and 'context'"}, 
                        status=status.HTTP_400_BAD_REQUEST)


    prompt = f"Title: {title}\nContext: {context}\n\nPlease break down the context into sections of approximately 50 words each, ensuring each sections forms a coherent idea."
    model = request.data.get("model", 'gpt-3.5-turbo-16k-0613')
    
    try:
        response = openai.ChatCompletion.create(model=model, 
                                                messages = [ 
                                                {'role': 'user', 'content': prompt}
                                                ],
                                                temperature=0,
                                                max_tokens=1000
                                                )

        segments = response["choices"][0]["message"]['content'].split('\n')
        usage = response["usage"]["total_tokens"]

        complete_segment = []

        for seg in segments:
            if seg.strip():
                segment_item = []
                segment = Segment(user=user, title=title, context=context, segment_text=seg)
                segment.save()
                print(segment)
                segment_item.append(segment.segment_text)
                video.segments.add(segment)
                video.save()
                # segment = generate_images(segments, "output_images")
                # saved_segments.append

                complete_segment.append(
                    {
                        "video_id": video.id,
                        "segment" : segment_item
                    }
                    )
        complete_segment.append({"token_count" : usage})

    
    except Exception as e:
        return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    # if not user_profile
    # user.token_usage
    # user.save()

    return Response(data=complete_segment, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_text(request):
    openai.api_key = OPENAIKEY

    try:
        prompt = request.data.get("prompt", 'What is the greatest team')
        model = request.data.get("model", 'text-davinci-003')
    except:
        raise Exception(f"No 'prompt' provided ")


    response = openai.Completion.create(model=f'{model}', 
                                    prompt=f'{prompt}', 
                                    temperature=0,
                                    max_tokens=10
                                    )
                                    

    output = response["choices"][0]["text"]

    return Response(data=output, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_flogi_ai_modules(request):

    openai.api_key = OPENAIKEY

    response = openai.Model.list()
    
    return Response(data=response, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_edit(request):

    prompt = request.data.get("prompt")
    instruction = request.data.get("instruction")

    openai.api_key = OPENAIKEY
    response = openai.Edit.create(
        model="text-davinci-edit-001",
        input= f'{prompt}',
        instruction=f'{instruction}'
    )

    return Response(data=response, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_image_create(request):

    openai.api_key = OPENAIKEY

    response = openai.Image.create(
                        prompt="A cute baby sea otter",
                        n=1,
                        size="512x512"
                        # user = ""
                        )

    return Response(data=response, status=200)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_image_edit(request):
    
    
    image = request.data.get("image")
    prompt = request.data.get("prompt")

    openai.api_key = OPENAIKEY

    response = openai.Image.create_edit(
            image=open(f'{image}', "rb"),
            # https://beta.openai.com/docs/api-reference/images/create-edit#images/create-edit-mask
            # mask=open("mask.png", "rb"),
            prompt=f'{prompt}',
            n=2,
            size="512x512"
            # user = ""
            )
                
    return Response(data=response, status=200)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_moderate(request):

    prompt = request.data.get("prompt")

    # prohibited_words = ["pork"]
    
    if prompt:
        # if prompt in prohibited_words:
        #     raise CustomException(detail="If you repeatedly try and save prohibeted words in attempt to break \
        #                              the law your account will be closed with immediete effect and reported \
        #                              to the police", \
        #                             status=status.HTTP_400_BAD_REQUEST)


        response = openai.Moderation.create(
                    input=f'{prompt}'
                    )

        openai.api_key = OPENAIKEY

        response = openai.Moderation.create(
                    input=f'{prompt}'
                    )
        output = response["results"][0]

        if response["results"][0]["flagged"] == False:
            pass
        
    return Response(data=output, status=200)




def flogi_google_saved_places(self, request):

    # Define your API key
    api_key = 'AIzaSyD9XJ7_na5NbWlapQ-ScsnuvbLJ0_s9mrk'

    # Create a client object
    client = googlemaps.Client(api_key)

    # Use the place() method to retrieve details about the authenticated user's saved places
    saved_places = client.place('user/me/saved')

        # Loop through the saved places and extract information about each place
    for place in saved_places['result']['items']:
        name = place['title']
        location = place['location']
        # Do something with the name and location of the saved place
        print(name)
        print(location)

