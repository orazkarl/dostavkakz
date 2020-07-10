from django.urls import path, include
from . import views

urlpatterns = [
    path('logout_user/', views.logout_user, name='logout_user'),
    path('accounts/password/change', views.CustomPasswordChangeView.as_view(), name='account_change_password'),
]
