from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
admin.site.site_header = 'JETKIZU.ME АДМИН ПАНЕЛЬ'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'paid', 'comment']
    filter_horizontal = ('items',)

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


# admin.site.register(OrderItem)

from allauth.account.admin import EmailAddress

from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
admin.site.unregister(EmailAddress)
admin.site.unregister(Group)
admin.site.unregister(Site)
