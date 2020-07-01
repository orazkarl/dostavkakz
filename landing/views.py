from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import JsonResponse, HttpResponse




class HomeView(TemplateView):
    template_name = 'landing/index.html'

