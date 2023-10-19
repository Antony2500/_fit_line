from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse

from shop.models import Product
from .models import Cart, CartItem
# Create your views here.


def cart(request):
    return render(request, "cart/cart.html")


def remove_from_cart(request):
    """
    Remove item from cart

    Видалення товара з кошика

    =========================================
    Add some code in js ( removeFromCart(e) )
    """
    data = json.loads(request.body)
    product_id = data["id"]

    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, completed=False)
    else:
        cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)

    product = get_object_or_404(Product, id=product_id)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity >= 1:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return JsonResponse({"message": "Product removed from cart"}, status=200)


def update_quantity(request):
    """
    Update quantity item in cart

    Оновити кількість товару в кошику

    ===================================
    Add some code in js ( changeQuantity(e) )
    """
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("id")
        change = data.get("change")

        try:
            product = Product.objects.get(id=product_id)

            # Получаем или создаем корзину для текущего пользователя
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            else:
                cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if change > 0:
                cart_item.quantity += 1
            elif change < 0 and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.save()

            return JsonResponse({"message": "Quantity updated successfully"})
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product not found"}, status=404)