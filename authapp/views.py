from django.shortcuts import render
from django.contrib import auth
from authapp.forms import ShopUserAuthenticationForm, ShopUserRegisterForm, ShopUserChangeForm, ShopUserProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from authapp.models import ShopUser


def login(request):
    login_form = ShopUserAuthenticationForm(data=request.POST)
    _next = request.GET.get('next', '')
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))
    context = {
        'login_form': login_form,
        'next': _next
    }
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    if request.method == 'POST':
        change_form = ShopUserChangeForm(request.POST, request.FILES, instance=request.user)
        change_profile_form = ShopUserProfileForm(request.POST, instance=request.user.shopuserprofile)
        if change_form.is_valid() and change_profile_form.is_valid():
            change_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))

    else:
        change_form = ShopUserChangeForm(instance=request.user)
        change_profile_form = ShopUserProfileForm(instance=request.user.shopuserprofile)
    context = {
        'title': 'Редактирование',
        'change_form': change_form,
        'change_profile_form': change_profile_form
    }
    return render(request, 'authapp/change.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return HttpResponseRedirect(reverse('authapp:login'))

    else:
        register_form = ShopUserRegisterForm()
    context = {
        'title': 'Регистрация',
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.activation_key_expired = None
            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verify.html')


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'
    message = f'{settings.BASE_URL}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
