from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.http import JsonResponse, HttpResponse
from .models import FoodTag, Store, Product, Review, Category
from user_auth.models import User, Address, StreetAdress, NumberHouseAddress
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.db.models import Q
from django.core import serializers

import requests
from bs4 import BeautifulSoup
import json


class HomeView(TemplateView):
    template_name = 'landing/index.html'


class StoresList(ListView):
    template_name = 'landing/stores_list.html'
    queryset = Store.objects.all()
    # model = Store

    def get(self, request, *args, **kwargs):


        store_category_slug = self.kwargs['slug']
        stores = Store.objects.filter(category__slug=store_category_slug)
        foodtags = FoodTag.objects.all()
        if request.GET:
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
            if 'avgcheck' in request.GET:
                avgcheck = request.GET['avgcheck']
                stores = stores.filter(avg_check=avgcheck)
            if store_category_slug == 'restoran':
                if 'foodcategory' in request.GET:
                    foodtag = request.GET.getlist('foodcategory')
                    stores = stores.filter(tag__id__in=foodtag).distinct('name')


        self.extra_context = {
            'stores': stores,
            'tags': foodtags,
            'slug': store_category_slug,
            'categories': Category.objects.all(),
        }
        return super().get(request, *args, **kwargs)

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
    template_name = 'landing/store_detail.html'

    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs.get(self.slug_url_kwarg, None)

        store = Store.objects.get(slug=store_slug)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                products = Product.objects.filter(store=store)
            else:
                products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(
                    category__tags__name__icontains=query)).filter(store=store).distinct('name')
            return render(request, 'landing/ajax_search_products.html', {'products': products, 'query': query})

        products = Product.objects.filter(store=store)
        print(products)
        reviews = Review.objects.filter(store=store)

        cart = Cart(request)
        items = []
        total_price = []
        print(cart.cart.values())
        for item in cart.cart.values():
            product_id = item['product_id']
            product = Product.objects.get(id=product_id)
            if store_slug == product.store.slug:
                item['description'] = product.description
                items.append(item)
                total_price.append(item['quantity'] * float(item['price']))
        total_price = sum(total_price)

        self.extra_context = {
            'products': products,
            'reviews': reviews,
            'items': items,
            # 'slug': slug,
            'total_price': total_price,

        }

        return super().get(request, *args, **kwargs)


# Cart
@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    store_slug = product.store.slug
    red = '/stores/detail/' + store_slug
    cart.add(product=product)
    return redirect(red)


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    slug = request.GET['slug']
    red = ''
    if request.GET['cart'] == 'true':
        red = '/stores/' + slug + '/cart'
    elif request.GET['cart'] == 'false':
        red = '/stores/detail/' + slug
    return redirect(red)


@login_required(login_url="/accounts/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    slug = request.GET['slug']
    red = ''
    if request.GET['cart'] == 'true':
        red = '/stores/' + slug + '/cart'
    elif request.GET['cart'] == 'false':
        red = '/stores/detail/' + slug
    return redirect(red)


@login_required(login_url="/accounts/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    slug = request.GET['slug']
    red = ''
    if request.GET['cart'] == 'true':
        red = '/stores/' + slug + '/cart'
    elif request.GET['cart'] == 'false':
        red = '/stores/detail/' + slug
    return redirect(red)


@login_required(login_url="/accounts/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    # slug = request.GET['slug']
    # red = '/stores/' + slug + '/cart'
    return redirect('/')


@login_required(login_url="/accounts/login")
def cart_detail(request, slug):
    cart = Cart(request)
    items = []
    total_price = []
    for item in cart.cart.values():
        product_id = item['product_id']
        product = Product.objects.get(id=product_id)
        print(type(item['quantity']))
        if product.name != item['name'] or float(product.price) != float(item['price']) or product.quantity < item['quantity']:
            cart.remove(product)
            break
        if slug == product.store.slug:
            item['description'] = product.description
            items.append(item)
            total_price.append(item['quantity'] * float(item['price']))
    store = Store.objects.get(slug=slug)
    total_price = sum(total_price)
    context = {
        'items': items,
        'store': store,
        'total_price': total_price,
    }
    return render(request, 'landing/cart_detail.html', context=context)






