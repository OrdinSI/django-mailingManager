from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm

from config.utils.mixins import StyleFormMixin
from users.models import User


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    """ Форма для аутентификации пользователя"""
    pass


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """ Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для профиля пользователя"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    """Форма для подтверждения смены пароля"""

    class Meta:
        model = User
        fields = ('email',)


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """Форма для смены пароля"""

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
