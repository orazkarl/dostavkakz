from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',  'total_price', 'paid', 'comment']
    filter_horizontal = ('items',)
admin.site.register(OrderItem)