from django.db import models
from user_auth.models import User
from landing.models import Product, Store

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField('Количество')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.item}"

# class OrderList(models.Model):
#     items = models.ManyToManyField(OrderItem, related_name='order_lists', verbose_name='Товары')
#
#     def __str__(self):
#         self.items

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Онлайн'),
        ('incash', 'Наличные'),
    ]

    DELIVERY_PAYMENT_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовызов')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Заведение')
    items = models.ManyToManyField(OrderItem, related_name='order_items', verbose_name='Товары', null=True, blank=True)
    total_price = models.DecimalField('Итоговая цена', max_digits=8, decimal_places=2)
    paid = models.BooleanField('Оплачен', default=False)
    payment_method = models.CharField('Способ оплаты', max_length=50, choices=PAYMENT_METHOD_CHOICES)
    delivery_method = models.CharField('Способ доставки', max_length=50, choices=DELIVERY_PAYMENT_CHOICES)
    address = models.CharField('Адрес', max_length=250, null=True, blank=True)
    comment = models.CharField('Комментария', max_length=250, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.user} - {self.total_price}"