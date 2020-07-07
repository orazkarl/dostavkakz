from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


def logout_user(request):
    logout(request)
    return redirect('home')
