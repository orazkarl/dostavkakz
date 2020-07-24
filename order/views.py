from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from cart.cart import Cart
from landing.models import Product, Store
from django.contrib.auth.decorators import login_required
from dostavkakz.settings import COURIER_TELEGRAM_BOT_TOKEN
import requests
from .models import OrderItem, Order


@login_required(login_url="/accounts/login")
def checkout(request, slug):
    cart = Cart(request)
    user = request.user
    store = Store.objects.get(slug=slug)
    order_comment = request.GET['order_comment']
    payment = request.GET['payment']
    address = user.address.first()
    address = str(address.address_name) + ', ' + str(address.number_house) + ' ' + 'кв/офис' + str(address.number_house)
    delivery_method = request.GET['delivery_method']
    total_price = []
    order_items = []
    for value in cart.cart.values():
        product_id = value['product_id']
        product = Product.objects.get(id=product_id)
        if store == product.store:
            price = int(value['quantity']) * float(value['price'])
            order_item = OrderItem.objects.create(user=user, item=product, quantity=value['quantity'], price=price)

            order_items.append(order_item)
            total_price.append(price)

        #     name = value['name']
        #     quantity = value['quantity']
        #     price = value['price']
        #     temp = 'Названия: ' + name + "\n" + 'Количество: ' + str(quantity) + "\n" + 'Цена: ' + str(quantity * float(price)) + "\n"
        #     message = message + temp + "\n"
        #     total_price.append(quantity * float(price))
    total_price = sum(total_price)
    order = Order.objects.create(user=user, store=store, total_price=total_price, payment_method=payment,
                                 delivery_method=delivery_method, address=address, comment=order_comment, paid=True)
    for item in order_items:
        order.items.add(item)
    order.save()
    response = telegramMessage(order)

    cart = Cart(request)
    cart.clear()

    return HttpResponse('Заказ принят')


def telegramMessage(order):
    message = 'Новый заказ!!!\n'
    for item in order.items.all():
        temp = 'Название: ' + str(item.item.name) + '\n'
        temp += 'Количество: ' + str(item.quantity) + '\n'
        # temp += 'Цена: ' + str(item.price) + '\n'
        message += temp
    message += '\n'
    message += 'Итого: ' + str(order.total_price) + '\n'
    message += 'Имя пользователя: ' + str(order.user.first_name) + ' ' + str(order.user.last_name) + '\n'
    message += 'Телефон: ' + str(order.user.phone) + '\n'
    message += 'Способ оплаты: ' + str(order.get_payment_method_display()) + '\n'
    paid = 'Нет'
    if order.paid:
        paid = 'Да'
    message += 'Оплачен: ' + paid + '\n'
    message += 'Способ доставки: ' + str(order.get_delivery_method_display()) + '\n'
    if order.delivery_method == 'delivery':
        message += 'Адрес: ' + str(order.address) + '\n'
    if order.comment != '':
        message += 'Комментария' + str(order.comment) + '\n'
    message += 'Дата: ' + str(order.created_date.day) + '.' + str(order.created_date.month) + '.' + str(
        order.created_date.year) + '\n'
    message += 'Время: ' + str(order.created_date.hour) + ':' + str(order.created_date.minute) + ':' + str(
        order.created_date.second) + '\n'

    requests.get("https://api.telegram.org/bot%s/sendMessage" % COURIER_TELEGRAM_BOT_TOKEN,
                 params={'chat_id': '-1001302242759', 'text': message})

    return 1
