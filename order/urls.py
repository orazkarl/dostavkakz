from django.urls import path, include
from . import views

urlpatterns = [
    path('stores/<slug:slug>/checkout/', views.checkout, name='checkout'),
]
