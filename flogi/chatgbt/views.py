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
from flogi.settings import OPENAIKEY
import json



# Create your views here.s
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_message(request):

    user = request.user
    try:
        prompt = request.data.get("prompt", 'What is the greatest team')
        model = request.data.get("model", 'gpt-3.5-turbo-16k-0613')
    except:
        raise Exception(f"No 'prompt' provided ")

    openai.api_key = OPENAIKEY
    
    response = openai.ChatCompletion.create(model=model, 
                                            messages = [ 
                                              {'role': 'user', 'content': prompt}
                                            ],
                                            temperature=0,
                                            max_tokens=10
                                            )
                                    

    output = response["choices"][0]["message"]['content']

    return Response(data=output, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flogi_ai_text(request):

    try:
        prompt = request.data.get("prompt", 'What is the greatest team')
        model = request.data.get("model", 'text-davinci-003')
    except:
        raise Exception(f"No 'prompt' provided ")

    openai.api_key = OPENAIKEY

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
                        n=2,
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

