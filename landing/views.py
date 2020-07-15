from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.http import JsonResponse, HttpResponse
from .models import FoodCategory, Store, Product, Review, Wishlist, Order
from user_auth.models import User, Address
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.db.models import Q
from django.core import serializers
from dostavkakz.settings import COURIER_TELEGRAM_BOT_TOKEN
import requests
from bs4 import BeautifulSoup
import json


class HomeView(TemplateView):
    template_name = 'landing/index.html'


class StoresList(ListView):
    template_name = 'landing/stores_list.html'
    queryset = Store.objects.all()

    def get(self, request, *args, **kwargs):
        stores = Store.objects.all()
        foodcategory = FoodCategory.objects.all().values_list('id', flat=True)

        if request.GET:
            if 'foodcategory' in request.GET:
                foodcategory = request.GET.getlist('foodcategory')
            stores = Store.objects.filter(tag__id__in=foodcategory).distinct('name')
            if 'avgcheck' in request.GET:
                avgcheck = request.GET['avgcheck']
                stores = stores.filter(avg_check=avgcheck)
            sort = request.GET['sortby']
            if sort == 'alphabet':
                stores = stores.order_by('name')
            if sort == 'inexpensive':
                stores = sorted(stores, key=lambda s: s.average_check())
                print(stores)
            if sort == 'expemsive':
                stores = reversed(sorted(stores, key=lambda s: s.average_check()))
            if sort == 'rating':
                stores = reversed(sorted(stores, key=lambda s: s.average_rating()))
        self.extra_context = {
            'stores': stores,
            'tags': FoodCategory.objects.all(),
        }
        return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return super().get(request, *args, **kwargs)


def search_stores(request):
    query = request.GET['q']
    results = Store.objects.filter(
        Q(description__icontains=query) | Q(name__icontains=query) | Q(address__icontains=query) | Q(
            tag__name__icontains=query)).distinct('name')
    if not query:
        results = ''
    return render(request, 'landing/ajax_search.html', {'results': results})


class StoreView(DetailView):
    model = Store
    template_name = 'landing/store_detile.html'

    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs.get(self.slug_url_kwarg, None)
        store = Store.objects.get(slug=store_slug)
        products = Product.objects.filter(store=store)
        reviews = Review.objects.filter(store=store)
        # if self.request.GET.get('q'):
        #     query = self.request.GET.get('q')
        #     if not query:
        #         return super().get(request, *args, **kwargs)
        #     products  = Product.objects.filter(store=store, name__icontains=query)
        self.extra_context = {
            'products': products,
            'reviews': reviews,
        }

        return super().get(request, *args, **kwargs)


# Cart
@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    store_slug = product.store.slug
    red = '/stores/' + store_slug
    cart.add(product=product)
    return redirect(red)


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)

    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login")
def cart_detail(request, slug):
    cart = Cart(request)
    items = []
    total_price = []
    for item in cart.cart.values():
        product_id = item['product_id']
        product = Product.objects.get(id=product_id)
        if slug == product.store.slug:
            items.append(item)
            total_price.append(item['quantity'] * float(item['price']))
    total_price = sum(total_price)
    context = {
        'items': items,
        'slug': slug,
        'total_price': total_price,
    }
    return render(request, 'landing/cart_detail.html', context=context)


@login_required(login_url="/accounts/login")
def checkout(request, slug):
    cart = Cart(request)
    total_price = []
    # message = """Новый заказ:\n"""
    message = ''

    for value in cart.cart.values():
        product_id = value['product_id']
        product = Product.objects.get(id=product_id)
        if slug == product.store.slug:
            name = value['name']
            quantity = value['quantity']
            price = value['price']
            temp = 'Названия: ' + name + "\n" + 'Количество: ' + str(quantity) + "\n" + 'Цена: ' + str(
                quantity * float(price)) + "\n"
            message = message + temp + "\n"
            total_price.append(quantity * float(price))

    total_price = sum(total_price)
    Order.objects.create(user=request.user, order_item=message, address='Адрес', total_price=total_price, status='1')
    message += 'Адрес: ' + "\n"
    message += 'ИТОГО: ' + str(total_price)

    requests.get("https://api.telegram.org/bot%s/sendMessage" % COURIER_TELEGRAM_BOT_TOKEN,
                 params={'chat_id': '-1001302242759', 'text': message})
    return HttpResponse('Заказ принят')


class WishlistView(ListView):
    template_name = 'landing/wishlist.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Wishlist.objects.filter(user_id=request.user.id)
        return super().get(request, *args, **kwargs)


def add_wishlist(request):
    user = request.user
    store_id = request.GET['store_id']
    # url = request.GET['url']

    item = get_object_or_404(Store, id=store_id)
    url = '/stores/' + item.slug
    if not Wishlist.objects.filter(user_id=user.id, store_item=item):
        Wishlist.objects.create(user_id=user.id, store_item=item)

    return redirect(url)


def del_wishlist(request):
    user = request.user
    store_id = request.GET['store_id']
    item = get_object_or_404(Store, id=store_id)

    if Wishlist.objects.filter(user_id=user.id, store_item=item):
        Wishlist.objects.filter(user_id=user.id, store_item=item).delete()

    return redirect('/wishlist')


class ProfileView(TemplateView):
    template_name = 'landing/profile.html'

    def post(self, request, *args, **kwargs):
        if request.POST:
            user = request.user
            if 'first_name' in request.POST:
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
            if 'username' in request.POST:
                user.username = request.POST['username']
                user.save()
        return super().get(request, *args, **kwargs)


class OrderView(ListView):
    template_name = 'landing/order.html'
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        self.queryset = Order.objects.filter(user=request.user)
        return super().get(request, *args, **kwargs)


class MyAddressView(TemplateView):
    template_name = 'landing/addresses.html'

    def post(self, request, *args, **kwargs):

        if request.POST:
            user = request.user
            if 'edit' in request.POST['type']:
                id = request.POST['address_id']
                new_address_name = request.POST['address_name']
                new_address_number_house = request.POST['address_number_house']
                new_address_number_apartment = request.POST['address_number_apartment']
                address = user.address.get(id=id)

                address.address_name = new_address_name
                address.number_house = new_address_number_house
                address.number_apartment = new_address_number_apartment
                address.save()
            if 'delete' in request.POST['type']:
                id = request.POST['address_id']
                address = user.address.get(id=id)
                address.delete()
            if 'add' in request.POST['type']:
                new_address_name = request.POST['address_name']
                new_address_number_house = request.POST['address_number_house']
                new_address_number_apartment = request.POST['address_number_apartment']
                if not Address.objects.filter(address_name=new_address_name, number_house=new_address_number_house,
                                              number_apartment=new_address_number_apartment, user=user):
                    Address.objects.create(address_name=new_address_name, number_house=new_address_number_house,
                                           number_apartment=new_address_number_apartment, user=user)
        return redirect('addresses')
        # return super().get(request, *args, **kwargs)
