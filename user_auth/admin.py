from django.contrib import admin
from .models import User, Address, StreetAdress, NumberHouseAddress
# Register your models here.



class AddressInline(admin.TabularInline):
    model = Address
    raw_id_fields = ['user']
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']

    inlines = [AddressInline]

admin.site.register(StreetAdress)
admin.site.register(NumberHouseAddress)