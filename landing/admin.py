from django.contrib import admin
from .models import *

@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'average_rating']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tag',)


admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)