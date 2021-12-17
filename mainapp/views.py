from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json
import random

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def user_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)


def get_random_hot():
    return random.choice(list(Product.objects.all()))


def get_same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


def index(request):
    products_list = Product.objects.all()[:4]
    context = {
        'title': 'Мой магазин',
        'products': products_list,
        'basket': user_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    title = 'Товары'
    if pk is not None:
        if pk == 0:
            product_list = Product.objects.all()
            category = {'name': 'все продукты'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=pk)
        context = {
            'product_list': product_list,
            'category': category,
            'title': title,
            'links_menu': links_menu,
            'basket': user_basket(request.user)
            }
        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_random_hot()
    context = {
        'links_menu': links_menu,
        'title': title,
        'basket': user_basket(request.user),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product)
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/json/contacts.json', encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты',
            'basket': user_basket(request.user)
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'basket': user_basket(request.user),
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk)
    }
    return render(request, 'mainapp/product.html', context)
