from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from allauth.account.views import PasswordChangeView
from django.urls import  reverse_lazy
from .models import Wishlist,User, Address, StreetAdress, NumberHouseAddress
from landing.models import Store, Product
from django.views.generic import TemplateView, ListView, DetailView

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

# class OrderView(ListView):
#     template_name = 'profile/order.html'
#     queryset = Order.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         self.queryset = Order.objects.filter(user=request.user)
#         return super().get(request, *args, **kwargs)


class HelpView(TemplateView):
    template_name = 'profile/help.html'


