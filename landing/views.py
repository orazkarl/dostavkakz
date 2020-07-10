from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.http import JsonResponse, HttpResponse
from .models import FoodCategory, Store, Product, Review, Wishlist, Order
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.db.models import Q
from django.core import serializers
from dostavkakz.settings import COURIER_TELEGRAM_BOT_TOKEN
import requests
from bs4 import BeautifulSoup


class HomeView(ListView):
    template_name = 'landing/index.html'
    queryset = Store.objects.all()

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'stores': Store.objects.all(),
        }
        return super().get(request, *args, **kwargs)


def search_stores(request):
    query = request.GET['q']
    if not query:
        return HttpResponse('')

    results = Store.objects.filter(
        Q(description__icontains=query) | Q(name__icontains=query) | Q(address__icontains=query) | Q(
            tag__name__icontains=query)).distinct('name')
    if results.count() == 0:
        return HttpResponse('')
    data = serializers.serialize('json', results)

    return HttpResponse(data, content_type="application/json")


class StoreView(DetailView):
    model = Store
    template_name = 'landing/store_deatil.html'

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
