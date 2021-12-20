from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopAdminUserChangeForm, ProductCategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'objects_list': ShopUser.objects.all().order_by('-is_active'),
    }
    return render(request, 'adminapp/users_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopAdminUserChangeForm(request.POST, request.FILES, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopAdminUserChangeForm(instance=current_user)
    context = {
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        context = {
            'object': current_user
        }
        return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'objects_list': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/categories_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm()
    context = {
        'form': form
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm(instance=category_item)
    context = {
        'form': form
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        current_category.is_active = False
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        context = {
            'object': current_category
        }
        return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'objects_list': Product.objects.filter(category__pk=pk),
        'category': ProductCategory(pk=pk)
    }
    return render(request, 'adminapp/products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        product_form = ProductForm()
    context = {
        'form': product_form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product_item)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
    else:
        product_form = ProductForm(instance=product_item)
    context = {
        'form': product_form,
        'category_pk': product_item.category.pk
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        current_product.is_active = False
        current_product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[current_product.category.pk]))
    else:
        context = {
            'object': current_product,
            'category_pk': current_product.category.pk
        }
        return render(request, 'adminapp/product_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    current_product = get_object_or_404(Product, pk=pk)
    context = {
        'product': current_product,
        'category_pk': current_product.category.pk
    }
    return render(request, 'adminapp/product.html', context)
