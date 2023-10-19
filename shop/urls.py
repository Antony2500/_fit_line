from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.shop, name="shop"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product_detail"),
]
