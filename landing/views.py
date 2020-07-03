from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import JsonResponse, HttpResponse
from .models import FoodCategory, Store, Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.db.models import Q
import json
from django.core import serializers

class HomeView(ListView):
    template_name = 'landing/index.html'
    queryset = Store.objects.all()

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'stores': Store.objects.all(),
        }
        text = 'д'

        return super().get(request, *args, **kwargs)



def search_stores(request):
    query = request.GET['q']
    if not query:
        return HttpResponse('')

    results = Store.objects.filter(Q(description__icontains=query) | Q(name__icontains=query) | Q(address__icontains=query) | Q(tag__name__icontains=query)).distinct('name')
    if results.count() == 0:
        return HttpResponse('')
    # results = Store.objects.annotate(search=SearchVector('description','name'),).filter(search=text)
    # l = []
    #
    # for store in Store.objects.all():
    #     print(text, store.tag.all())
    #     if text.lower() in str(store.tag.all()).lower():
    #         l.append(store)
    # context = {'stores' : l}
    context = {
        'results_search' : results,
    }

    data = serializers.serialize('json', results)
    # res = {"results_search": data}
    # return JsonResponse(res)
    return HttpResponse(data, content_type="application/json")
    # return render(request, 'landing/base.html', context)
class StoreView(DetailView):
    model = Store
    template_name = 'landing/store_deatil.html'

    def get(self, request, *args, **kwargs):
        store_slug = self.kwargs.get(self.slug_url_kwarg, None)
        store = Store.objects.get(slug=store_slug)

        products = Product.objects.filter(store=store)
        # if self.request.GET.get('q'):
        #     query = self.request.GET.get('q')
        #     if not query:
        #         return super().get(request, *args, **kwargs)
        #     products  = Product.objects.filter(store=store, name__icontains=query)
        self.extra_context = {
            'products': products,
        }

        return super().get(request, *args, **kwargs)


# Cart
@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    store_slug = product.store.slug
    red = '/store/' + store_slug
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
def cart_detail(request):
    return render(request, 'landing/cart_detail.html')
