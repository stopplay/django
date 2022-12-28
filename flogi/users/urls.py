from django.shortcuts import render

from django.urls import path
from users.views import RegisterView, LoginView, UserView, LogoutView





app_name = 'users'
urlpatterns = [
    path('register', RegisterView.as_view, name='Register'),
    path('login', LoginView.as_view, name='Login'),
    path('users', UserView.as_view, name='Users'),
    path('logout', LogoutView.as_view, name='Logout')
]