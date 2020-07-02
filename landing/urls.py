from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('store/<slug:slug>', views.StoreView.as_view(), name='store_detail'),
]
