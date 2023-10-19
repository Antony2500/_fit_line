from django.urls import path
from . import views

urlpatterns = [
    path("cart", views.cart, name="cart"),
    path("remove_from_cart", views.remove_from_cart, name="remove_from_cart"),
    path("update_quantity", views.update_quantity, name='update_quantity'),
]
