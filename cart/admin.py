from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import Cart, CartItem


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'completed', 'session_id', 'creation_time']


@admin.register(CartItem)
class CartItemModelAdmin(admin.ModelAdmin):
    list_display = ['products', 'cart', 'quantity']

    def products(self, obj):
        link = reverse("admin:shop_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.name)
