from django.urls import path, include
from . import views
from allauth.account import views as account_views
urlpatterns = [
    #account
    path('logout_user/', views.logout_user, name='logout_user'),
    path('signup/',  views.sign_up, name='signup'),
    path('password/reset/',  views.reset_password, name='reset_password'),

    path('login/',  account_views.login, name='account_login'),
    path('signup/',  account_views.signup, name='account_signup'),
    # path('password/reset',  account_views.signup, name='account_reset_password'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='account_change_password'),

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
