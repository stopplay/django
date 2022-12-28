from django.urls import include, path
from . import views


app_name = 'chatgbt'
urlpatterns = [
    path('get_flogi_ai_modules/', views.get_flogi_ai_modules, name='Get ChatGBT Models'),
    path('flogi_ai/', views.flogi_ai, name='Flogi AI'),
    path('flogi_ai_moderate/', views.flogi_ai_moderate, name='Flogi AI Moderate'),
    path('flogi_ai_edit/', views.flogi_ai_edit, name='Flogi AI Edit'),
    path('flogi_ai_image_create/', views.flogi_ai_image_create, name='Flogi AI Image Create'),
    path('flogi_ai_image_edit/', views.flogi_ai_image_edit, name='Flogi AI Image edit'),
]