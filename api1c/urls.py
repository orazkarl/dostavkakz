from django.urls import path, include
from . import views
urlpatterns = [
    path('product/create/', views.ProductCreateView.as_view()),
]

