from django.urls import include, path
from . import views
from rest_framework import routers


app_name = 'chatgbt'
urlpatterns = [
    path('get-flogi-ai-modules/', views.get_flogi_ai_modules, name='Get ChatGBT Models'),
    path('flogi-ai-text/', views.flogi_ai_text, name='Flogi AI'),
    path('flogi-ai-gpt3-5-turbo/', views.flogi_ai_message, name='Flogi AI ChatGPT 3.5'),
    path('flogi-ai-moderate/', views.flogi_ai_moderate, name='Flogi AI Moderate'),
    path('flogi-ai-edit/', views.flogi_ai_edit, name='Flogi AI Edit'),
    path('flogi-ai-image-create/', views.flogi_ai_image_create, name='Flogi AI Image Create'),
    path('flogi-ai-image-edit/', views.flogi_ai_image_edit, name='Flogi AI Image edit'),
]