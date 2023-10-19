from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from shop.models import Product, CATEGORY_CHOICES
from . import templates

# Create your views here.


def index(request):
    context = {
        'active_page': 'home'
    }
    return render(request, 'main_pages/index.html', context)


def search(request):
    """

    """
    query = request.GET.get('search', '')

    # Разбиваем запрос на отдельные слова
    search_terms = query.split()

    # Создаем пустое Q-условие
    search_condition = Q()

    # Добавляем условие для поиска по названию продукта
    for term in search_terms:
        search_condition |= Q(name__icontains=term)

    # Для каждой категории в CATEGORY_CHOICES
    for category_set in CATEGORY_CHOICES:
        # Преобразуем множество в строку
        category_string = ' '.join(category_set[1:])

        # Проверяем, содержатся ли введенные пользователем слова в этой строке
        for term in search_terms:
            if term.lower() in category_string.lower():
                # Если слово найдено, добавляем его в условие OR
                search_condition |= Q(category=category_set[0])
                break

    # Ищем продукты, соответствующие условию
    products = Product.objects.filter(search_condition)

    context = {
        'products': products
    }

    # Здесь возвращается JSON с результатами поиска
    search_results = render_to_string('web-site_fit_line2/search_results.html', context)
    return JsonResponse({'search_results': search_results})


def about(request):
    context = {
        'active_page': 'about'
    }
    return render(request, 'main_pages/about.html', context)


def contact(request):
    context = {
        'active_page': 'contact'
    }
    return render(request, 'main_pages/contact.html', context)
