from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Wishlist, User, Address, StreetAdress, NumberHouseAddress
from landing.models import Store, Product
from django.views.generic import TemplateView, ListView, DetailView
from order.models import Order
from .forms import  UserCreateForm, UserResetPasswordForm
import random
import string

import requests

MOBIZON_API_KEY = 'kz79254c7b79ab00e882f92418131e194df3783a54052356ff64a2623c9f40a19e8ca6'
DOMEN_API = 'api.mobizon.kz'

def genetate_password(length=8):
    possible_characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    random_character_list = [random.choice(possible_characters) for i in range(length)]
    random_password = "".join(random_character_list)
    return random_password

def sign_up(request):
    if request.POST:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = genetate_password()
            print(password)
            url = 'https://api.mobizon.kz/service/message/sendsmsmessage?' \
                  'recipient=' + str(phone).split('+')[1] + '&' \
                                                            'text=Vash+parol+dlya+vhoda:+' + password + \
                  '&apiKey=' + MOBIZON_API_KEY
            requests.get(url=url)
            username = str(phone)
            user = User.objects.create_user(username=username, phone=phone, password=password, first_name=first_name,
                                            last_name=last_name, email=email)
            return HttpResponse('success')
        else:
            return HttpResponse(str(form.errors))
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


def reset_password(request):
    if request.POST:
        form = UserResetPasswordForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            try:
                user = User.objects.get(phone=phone)
            except Exception:
                return HttpResponse('Пользователь не существует')
            new_password = genetate_password()
            print(new_password)
            user.set_password(new_password)
            user.save()
            url = 'https://api.mobizon.kz/service/message/sendsmsmessage?' \
                  'recipient=' + str(phone).split('+')[1] + '&' \
                                                            'text=Vash+parol+dlya+vhoda:+' + new_password + \
                  '&apiKey=' + MOBIZON_API_KEY
            requests.get(url=url)
            return HttpResponse('success')
        else:
            return HttpResponse(str(form.errors))
    else:
        form = UserResetPasswordForm()
    return render(request, 'registration/password_reset.html', {'form': form})
def logout_user(request):
    logout(request)
    return redirect('home')


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('profile')


class WishlistView(ListView):
    template_name = 'profile/wishlist.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Wishlist.objects.filter(user_id=request.user.id)
        return super().get(request, *args, **kwargs)


def add_wishlist(request):
    user = request.user
    store_id = request.GET['store_id']
    # url = request.GET['url']
    # slug = request.GET['slug']
    item = get_object_or_404(Store, id=store_id)
    url = '/stores/detail/' + item.slug
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
    template_name = 'profile/profile.html'

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


class MyAddressView(ListView):
    template_name = 'profile/addresses.html'
    model = User

    def get(self, request, *args, **kwargs):
        houses = ''
        print(request.GET)
        if request.GET:
            street = request.GET['street']
            houses = NumberHouseAddress.objects.filter(street=street)
            return render(request, 'profile/ajax_address_list.html', {'houses': houses})
        self.queryset = Address.objects.filter(user=request.user)
        self.extra_context = {
            'streets': StreetAdress.objects.all(),
            'houses': houses,
        }

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST:
            user = request.user
            if 'edit' in request.POST['type']:
                id = request.POST['address_id']
                new_address_name = request.POST['address_name']
                new_address_number_house = request.POST['address_number_house']
                new_address_number_apartment = request.POST['address_number_apartment']
                address = user.address.get(id=id)
                if 'save' in request.POST:
                    address.address_name = new_address_name
                    address.number_house = new_address_number_house
                    address.number_apartment = new_address_number_apartment

                    address.save()
            if 'delete' in request.POST['type']:
                id = request.POST['address_id']
                address = user.address.get(id=id)
                address.delete()
            if 'add' in request.POST['type']:
                if 'save' in request.POST:
                    new_address_name = StreetAdress.objects.get(id=request.POST['street'])
                    new_address_number_house = NumberHouseAddress.objects.get(id=request.POST['house'])
                    new_address_number_apartment = request.POST['address_number_apartment']
                    if not Address.objects.filter(address_name=new_address_name, number_house=new_address_number_house,
                                                  number_apartment=new_address_number_apartment, user=user):
                        Address.objects.create(address_name=new_address_name, number_house=new_address_number_house,
                                               number_apartment=new_address_number_apartment, user=user)

        return redirect('addresses')
        # return super().get(request, *args, **kwargs)


class OrderView(ListView):
    template_name = 'profile/order.html'
    queryset = Order.objects.all()

    def get(self, request, *args, **kwargs):
        self.queryset = Order.objects.filter(user=request.user).order_by('-created_date')
        return super().get(request, *args, **kwargs)


class HelpView(TemplateView):
    template_name = 'profile/help.html'
