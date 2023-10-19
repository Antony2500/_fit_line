from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Customer


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'amount', 'status', 'ordering_method', 'creation_time', 'comment',
                    'completed', 'shipping_address']


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_id', 'name', 'surname', 'email', 'mobile', 'state', 'city',
                    'branch_number']
