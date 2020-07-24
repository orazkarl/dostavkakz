from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FoodTag)
class FoodTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'average_rating', 'average_check']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tag',)


admin.site.register(Product)
admin.site.register(Review)

