from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search_stores, name='search_stores'),
    path('stores/<slug:slug>', views.StoreView.as_view(), name='store_detail'),

    # cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('stores/<slug:slug>/cart', views.cart_detail, name='cart_detail'),

    #
    path('stores/<slug:slug>/checkout/' , views.checkout, name='checkout'),

    # wishist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('del_wishlist/', views.del_wishlist, name='del_wishlist'),

    # profile
    path('profile', views.ProfileView.as_view(), name='profile'),

]
