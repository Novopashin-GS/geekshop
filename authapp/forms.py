from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import HiddenInput

from authapp.models import ShopUser


class ShopUserAuthenticationForm(AuthenticationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserChangeForm(UserChangeForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'password', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = HiddenInput()
