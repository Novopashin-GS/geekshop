from django.shortcuts import render
from django.conf import settings
import json
from mainapp.models import Product, ProductCategory


def index(request):
    products_list = Product.objects.all()[:4]
    context = {
        'title': 'Мой магазин',
        'products': products_list
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/json/contacts.json', encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты'
        }
    return render(request, 'mainapp/contact.html', context)
