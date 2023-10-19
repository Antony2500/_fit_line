import uuid

from django.contrib.auth.models import User
from django.db import models

from shop.models import Product

# Create your models here.
AREA_CHOICES = (
    ('Vinnytsia Oblast', 'Vinnytsia Oblast'),
    ('Volyn Oblast', 'Volyn Oblast'),
    ('Dnipropetrovsk Oblast', 'Dnipropetrovsk Oblast'),
    ('Donetsk Oblast', 'Donetsk Oblast'),
    ('Zhytomyr Oblast', 'Zhytomyr Oblast'),
    ('Zakarpattia Oblast', 'Zakarpattia Oblast'),
    ('Zaporizhia Oblast', 'Zaporizhia Oblast'),
    ('Ivano-Frankivsk Oblast', 'Ivano-Frankivsk Oblast'),
    ('Kyiv Oblast', 'Kyiv Oblast'),
    ('Kirovohrad Oblast', 'Kirovohrad Oblast'),
    ('Luhansk Oblast', 'Luhansk Oblast'),
    ('Lviv Oblast', 'Lviv Oblast'),
    ('Mykolaiv Oblast', 'Mykolaiv Oblast'),
    ('Odessa Oblast', 'Odessa Oblast'),
    ('Poltava Oblast', 'Poltava Oblast'),
    ('Rivne Oblast', 'Rivne Oblast'),
    ('Sumy Oblast', 'Sumy Oblast'),
    ('Ternopil Oblast', 'Ternopil Oblast'),
    ('Kharkiv Oblast', 'Kharkiv Oblast'),
    ('Kherson Oblast', 'Kherson Oblast'),
    ('Khmelnytskyi Oblast', 'Khmelnytskyi Oblast'),
    ('Cherkasy Oblast', 'Cherkasy Oblast'),
    ('Chernivtsi Oblast', 'Chernivtsi Oblast'),
    ('Chernihiv Oblast', 'Chernihiv Oblast'),
    ('Kyiv City', 'Kyiv City'),
    ('Autonomous Republic of Crimea', 'Autonomous Republic of Crimea'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=30,  default='')
    surname = models.CharField(max_length=30, default='')
    state = models.CharField(choices=AREA_CHOICES, max_length=100)
    city = models.CharField(max_length=50)
    branch_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default='')
    mobile = models.CharField(max_length=20, default='+38', blank=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    STATUS_ORDERING_PROCESS = '1_ordering_process'
    STATUS_WAITING_FOR_ACCEPT = '2_waiting_for_accept'
    STATUS_ACCEPTED = '3_accepted'
    STATUS_DELIVERING = '4_delivering'
    STATUS_DELIVERED = '5_delivered'
    STATUS_RECEIVED = '6_received'

    STATUS_CHOICES = [
        (STATUS_ORDERING_PROCESS, 'cart'),
        (STATUS_WAITING_FOR_ACCEPT, 'waiting for accept'),
        (STATUS_ACCEPTED, 'accepted'),
        (STATUS_DELIVERING, 'delivering'),
        (STATUS_DELIVERED, 'delivered'),
        (STATUS_RECEIVED, 'received'),
    ]

    CATEGORY_ORDERING_METHOD = (
        ('CP', 'Оплата на карту'),
        ('PUC', 'Оплата при отриманні')
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=STATUS_ORDERING_PROCESS)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    ordering_method = models.CharField(choices=CATEGORY_ORDERING_METHOD, max_length=3, default="CP")
    comment = models.TextField(blank=True)
    shipping_address = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    @property
    def order_total_price(self):
        order_items = self.order_items.all()
        total = sum([item.price for item in order_items])
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=2)