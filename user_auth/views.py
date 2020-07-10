from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from allauth.account.views import PasswordChangeView
from django.urls import  reverse_lazy


def logout_user(request):
    logout(request)
    return redirect('home')

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')
