from django.urls import path, include
from . import views

urlpatterns = [
    path('logout_user/', views.logout_user, name='logout_user'),
    path('accounts/password/change', views.CustomPasswordChangeView.as_view(), name='account_change_password'),

    # wishist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('del_wishlist/', views.del_wishlist, name='del_wishlist'),

    # profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('addresses/', views.MyAddressView.as_view(), name='addresses'),
    path('help/', views.HelpView.as_view(), name='help')
]
