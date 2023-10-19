from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Order, OrderItem, Customer
from cart.models import Cart
from .forms import CustomerProfileForm, DeliveryMethod
# Create your views here.


def order(request):
    """
    Creating an order and sending it to the database

    Створення замовлення та відправка його в базу даних

    Returns:
        Order: return customer form and order

    ========================================================
    add @property order_total_price(self)
    """
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.get(session_id=request.session['nonuser'])

    try:
        order = Order.objects.get(user=cart.user, session_id=cart.session_id, status=Order.STATUS_WAITING_FOR_ACCEPT)
        order.order_items.all().delete()
    except Order.DoesNotExist:
        # Если заказ не существует, создайте новый
        order = Order(user=cart.user, session_id=cart.session_id, status=Order.STATUS_WAITING_FOR_ACCEPT)
        order.save()

    for cart_item in cart.cart_items.all():
        order_item, created = OrderItem.objects.get_or_create(order=order, product=cart_item.product, price=0)
        order_item.quantity = cart_item.quantity
        order_item.price = cart_item.price
        order_item.save()

    order.amount = order.order_total_price

    customer_profile_form = CustomerProfileForm()
    delivery_method_form = DeliveryMethod()

    if request.method == 'POST':
        customer_profile_form = CustomerProfileForm(request.POST)
        delivery_method_form = DeliveryMethod(request.POST)

        if customer_profile_form.is_valid() and delivery_method_form.is_valid():
            # Customer Profile Form
            name = customer_profile_form.cleaned_data['name']
            surname = customer_profile_form.cleaned_data['surname']
            email = customer_profile_form.cleaned_data['email']
            mobile = customer_profile_form.cleaned_data['mobile']
            state = customer_profile_form.cleaned_data['state']
            city = customer_profile_form.cleaned_data['city']
            branch_number = customer_profile_form.cleaned_data['branch_number']

            # Delivery Method Form
            ordering_method = delivery_method_form.cleaned_data['ordering_method']
            comment = delivery_method_form.cleaned_data['comment']

            reg = Customer(user=order.user, session_id=order.session_id, name=name, surname=surname,
                           email=email, mobile=mobile, state=state, city=city,
                           branch_number=branch_number)

            order.ordering_method = ordering_method
            order.comment = comment
            order.shipping_address = reg
            order.status = Order.STATUS_ACCEPTED
            reg.save()
            order.save()
            cart.delete()
            messages.success(request, "Вітаю! Адресу успішно збережено")

            subject = 'Ваше замовлення на сайті Fit line отримано'
            message_for_email = f'Ваше замовлення отримано. \
            Підтвердження наявності товару зазначеного у Вашому \
            замовленні, відбувається протягом 24 годин з моменту \
            оформлення замовлення, у вихідні дні протягом 48 годин. \
            {order.id} \
            Загальна сума: {order.amount}.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            return render(request, 'order/order_done.html')
        else:
            messages.warning(request, "Неправильні вхідні дані")

    context = {
        'order': order,
        'customer_profile_form': customer_profile_form,
        'delivery_method_form': delivery_method_form,
    }

    return render(request, "order/order.html", context)


def order_done(request):
    return render(request, "order/order_done")