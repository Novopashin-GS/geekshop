from django.shortcuts import render
from django.conf import settings
import json


def index(request):
    context = {
        'title': 'Мой магазин'
    }
    return render(request, 'mainapp/index.html', context)


links_menu = [
    {"href": 'products', 'name': 'Все'},
    {"href": 'products_home', 'name': 'Дом'},
    {"href": 'products_modern', 'name': 'Модерн'},
    {"href": 'products_office', 'name': 'Оффис'},
    {"href": 'products_classic', 'name': 'Классика'},
]


def products(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def products_home(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def products_office(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def products_modern(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def products_classic(request):
    context = {
        'links_menu': links_menu,
        'title': 'Товары'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/contacts.json', encoding='utf-8') as contacts_file:
        context = {
            'contacts': json.load(contacts_file),
            'title': 'Контакты'
        }
    return render(request, 'mainapp/contact.html', context)
