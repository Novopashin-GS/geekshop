from django.shortcuts import render
from django.contrib import auth
from authapp.forms import ShopUserAuthenticationForm, ShopUserRegisterForm, ShopUserChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def login(request):
    login_form = ShopUserAuthenticationForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'login_form': login_form
    }
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    if request.method == 'POST':
        change_form = ShopUserChangeForm(request.POST, request.FILES, instance=request.user)
        if change_form.is_valid():
            change_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))

    else:
        change_form = ShopUserChangeForm(instance=request.user)
    context = {
        'change_form': change_form
    }
    return render(request, 'authapp/change.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))

    else:
        register_form = ShopUserRegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)
