from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import JsonResponse, HttpResponse
from .models import FoodCategory, Store, Product



class HomeView(ListView):
    template_name = 'landing/index.html'
    queryset = Store.objects.all()
    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'stores': Store.objects.all(),
        }
        return super().get(request, *args, **kwargs)

class StoreView(DetailView):
    model = Store
    template_name = 'landing/store_deatil.html'
    def get(self, request, *args, **kwargs):
        store_slug =self.kwargs.get(self.slug_url_kwarg, None)
        store = Store.objects.get(slug=store_slug)

        products = Product.objects.filter(store=store)
        # if self.request.GET.get('q'):
        #     query = self.request.GET.get('q')
        #     if not query:
        #         return super().get(request, *args, **kwargs)
        #     products  = Product.objects.filter(store=store, name__icontains=query)
        self.extra_context = {
            'products' : products,
        }

        return super().get(request, *args, **kwargs)


