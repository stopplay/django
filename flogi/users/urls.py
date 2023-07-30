from django.shortcuts import render

from django.urls import path
from users.views import RegisterView, LoginView, UserView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='Register'),
    path('login/', LoginView.as_view(), name='Login'),
    path('user/', UserView.as_view(), name='Users'),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]