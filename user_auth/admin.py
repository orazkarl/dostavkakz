from django.contrib import admin
from .models import User, Address, StreetAdress, NumberHouseAddress
# Register your models here.



class AddressInline(admin.TabularInline):
    model = Address
    raw_id_fields = ['user']
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone']

    fieldsets = (
        (None,
         {'fields': ('username', 'email')}),
        (('Личная информация'),
         {'fields': (
             'first_name', 'last_name', 'phone')}),
        (('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Дата и время', {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [AddressInline]


admin.site.register(StreetAdress)
admin.site.register(NumberHouseAddress)