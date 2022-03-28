from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authapp.models import ShopUser


@admin.register(ShopUser)
class CustomUser(UserAdmin):
    list_display = ('username', 'email')

