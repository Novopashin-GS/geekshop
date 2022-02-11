from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.conf import settings
import json
import random
from django.core.cache import cache
from mainapp.models import Product, ProductCategory
from django.views.decorators.cache import cache_page


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_products_in_category(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_pk_{pk}'
        product_list = cache.get(key)
        if product_list is None:
            product_list = Product.objects.filter(is_active=True, category__pk=pk).select_related()
            cache.set(key, product_list)
        return product_list
    else:
        return Product.objects.filter(is_active=True, category__pk=pk).select_related()


def get_random_hot():
    return random.choice(list(Product.objects.filter(is_active=True)))


def get_same_products(hot_product):
    return Product.objects.filter(is_active=True, category=hot_product.category).exclude(pk=hot_product.pk)[:3]


def index(request):
    products_list = Product.objects.filter(is_active=True)[:4]
    context = {
        'title': 'Мой магазин',
        'products': products_list,
    }
    return render(request, 'mainapp/index.html', context)


#@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()
    title = 'Товары'
    if pk is not None:
        if pk == 0:
            product_list = Product.objects.filter(is_active=True)
            category = {'name': 'все продукты', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = get_products_in_category(pk)
        paginator = Paginator(product_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)
        context = {
            'product_list': products_paginator,
            'category': category,
            'title': title,
            'links_menu': links_menu,
            }
        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_random_hot()
    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product)
    }
    return render(request, 'mainapp/products.html', context)


#@cache_page(3600)
def contact(request):
    with open(f'{settings.BASE_DIR}/json/contacts.json', encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты',
        }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = get_links_menu()
    context = {
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk)
    }
    return render(request, 'mainapp/product.html', context)
