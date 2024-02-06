from django.urls import include, path
from . import views
from rest_framework import routers


app_name = 'chatgbt'
urlpatterns = [
    path('get-flogi-ai-modules/', views.get_flogi_ai_modules, name='Get ChatGBT Models'),
    path('flogi-ai-text/', views.flogi_ai_text, name='Flogi AI'),
    path('flogi-ai-story-create/', views.flogi_story_segments, name='Create Story and Segments'),
    path('flogi-ai-moderate/', views.flogi_ai_moderate, name='Flogi AI Moderate'),
    path('flogi-ai-edit/', views.flogi_ai_edit, name='Flogi AI Edit'),
    path('flogi-ai-image-create/', views.flogi_ai_image_create, name='Flogi AI Image Create'),
    path('flogi-ai-image-edit/', views.flogi_ai_image_edit, name='Flogi AI Image edit'),
    path('flogi-segments/', views.get_all_segments, name='Segments'),
    path('flogi-video-create/', views.flogi_create_video, name="Create Video"),
    path('flogi-videos/', views.get_all_videos, name='Videos'),
    path('flogi-generate-images-for-segments/', views.flogi_generate_images_for_segments, name="Generate Images"),
    path('flogi-get-video/<int:pk>', views.get_flogi_video, name='Get Video'),
         ]