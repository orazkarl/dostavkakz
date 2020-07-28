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
    list_display = ['name', 'address', 'description', 'average_rating', 'average_check']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tag',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'store', 'description', 'price']
    list_filter = ['store']
    ordering = ['store']
# admin.site.register(Review)
