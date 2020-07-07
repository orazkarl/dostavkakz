from django.urls import path, include
from . import views

urlpatterns = [
    path('logout_user/', views.logout_user, name='logout_user'),
]
