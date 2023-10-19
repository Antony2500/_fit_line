import uuid
import json
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from cart.models import Cart, CartItem
from .models import Product, CATEGORY_CHOICES
from django.db.models import Count

# Create your views here.


# Function for product filtering and search ( Функція фільтрації та пошуку товарів )
def shop(request):
    """
    Function for product filtering and search :

    Search by name and CATEGORY_CHOICES; Filter by min_price, max_price, category, manufacturer; Sort by price-asc,
    price-desc, name-asc, name-desc.


    Функція фільтрації та пошуку товарів

    Пошук за назвою та CATEGORY_CHOICES; Фільтр за min_price, max_price, категорією, виробником; Сортування за price-asc,
    price-desc, name-asc, name-desc.
    """
    if request.method == 'GET':

        # Receiving a request ( Отримання запросу )
        query = request.GET.get('search', '')

        # Break down the query into individual words ( Розбиваєм запит на окремі слова )
        search_terms = query.split()

        # Create an empty Q-condition ( Створіть порожню Q-умову )
        search_condition = Q()

        # Search by product name ( Пошук за назвою товару )
        for term in search_terms:
            search_condition |= Q(name__icontains=term)

        # Search by product category in CATEGORY_CHOICES ( Пошук за категорією товару в CATEGORY_CHOICES )
        for category_set in CATEGORY_CHOICES:
            # Convert the set to a string ( Перетворюємо множество в рядок )
            category_string = ' '.join(category_set[1:])

            # Check if the words entered by the user are contained in this string
            # Перевірити, чи містяться слова, введені користувачем, у цьому рядку
            for term in search_terms:
                if term.lower() in category_string.lower():
                    search_condition |= Q(category=category_set[0])
                    break

        products = Product.objects.filter(search_condition)

        # Check if the resetFilters parameter is present and reset the filters
        # Перевіряємо, чи присутній параметр resetFilters, і скидуємо фільтри
        if 'resetFilters' in request.GET:
            return redirect('shop')

        # Variables for filters (get values from GET-request) ( Змінні для фільтрів (отримують значення з GET-запиту) )
        min_price = request.GET.get('minPrice')
        max_price = request.GET.get('maxPrice')
        category = request.GET.get('category')
        manufacturer = request.GET.get('manufacturer')

        # Filtering of goods based on passed filters ( Фільтрація товарів на основі пройдених фільтрів )
        if category and category != "":
            products = products.filter(category=category)
        if manufacturer and manufacturer != "":
            products = products.filter(manufacturer=manufacturer)
        if min_price and min_price.isdigit():
            products = products.filter(selling_price__gte=min_price)
        if max_price and max_price.isdigit():
            products = products.filter(selling_price__lte=max_price)

        # Get the sort parameter from the GET request ( Отримуємо параметр sort з GET-запиту)
        sort_by = request.GET.get('sort', '')
        if sort_by == 'price-asc':
            products = products.order_by('selling_price')
        elif sort_by == 'price-desc':
            products = products.order_by('-selling_price')
        elif sort_by == 'name-asc':
            products = products.order_by('name')
        elif sort_by == 'name-desc':
            products = products.order_by('-name')

        # Getting unique values of categories and manufacturers for filters
        # Отримуємо унікальні значення категорій і виробників для фільтрів
        categories = Product.objects.values_list('category', flat=True).distinct()
        manufacturers = Product.objects.values_list('manufacturer', flat=True).distinct()

        return render(request, 'shop/shop.html', {'products': products, 'min_price': min_price,
                                                  'max_price': max_price, 'category': category,
                                                  'manufacturer': manufacturer, 'categories': categories,
                                                  'manufacturers': manufacturers})

    else:
        # If the request is not a GET request, perform the appropriate action
        # Якщо запит не є GET-запитом, виконайте відповідну дію
        return HttpResponseNotAllowed(['GET'])


# Class for displaying product information ( Клас для відображення інформації про товар )
class ProductDetail(View):
    """
    Class for displaying product information

    Клас для відображення інформації про товар
    """
    template_name = 'shop/product_detail.html'

    def get_context_data(self, pk):
        """
        Receiving the product by PK

        Отримання продукта за PK

        Returns:
            context: Selected product for PK ( Отриманний продукт за PK )
        """
        product = get_object_or_404(Product, pk=pk)
        context = {
            'product': product,
        }
        return context

    def get(self, request, pk):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if request.user.is_authenticated:
            # Order.amount = Cart.amount
            cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
            cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_items.quantity += 1
            cart_items.save()
        else:

            try:
                cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
                cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cart_items.quantity += 1
                cart_items.save()
            except:
                request.session['nonuser'] = str(uuid.uuid4())
                cart = Cart.objects.create(session_id=request.session['nonuser'], completed=False)
                cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
                cart_items.quantity += 1
                cart_items.save()

        return redirect('cart')


# The function of adding an item to the cart ( Функція додавання товару в кошик )
def add_to_cart(request):
    """
    Adding an item to the cart

    Додавання товару в кошик

    =======================================
    Add some code in js (function addToCart(e))
    """
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        # Order.amount = Cart.amount
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_items.quantity += 1
        cart_items.save()
    else:

        try:
            cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
            cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_items.quantity += 1
            cart_items.save()

        except:
            request.session['nonuser'] = str(uuid.uuid4())
            cart = Cart.objects.create(session_id=request.session['nonuser'], completed=False)
            cart_items, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_items.quantity += 1
            cart_items.save()

    return JsonResponse("it is working", safe=False)

# class CategoryView(View):
#     def get(self, request, val):
#         product = Product.objects.filter(category=val)
#         title = Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
#         context = {
#             'products': product,
#             'titles': title,
#         }
#         return render(request, "shop/category.html", {'product': product, 'title': title})
#
#
# class CategoryTitle(View):
#     def get(self, request, val):
#         product = Product.objects.filter(title=val)
#         title = Product.objects.filter(category=product[0].category).values('title')
#         context = {
#             'products': product,
#             'titles': title,
#         }
#         return render(request, "shop/category.html", {'product': product, 'title': title})
