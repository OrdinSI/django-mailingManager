from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, \
    UserChangeForm
from users.models import User
import pytz

from utils.mixins import StyleFormMixin


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
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in pytz.all_timezones])

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'timezone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UpdateUserForm(StyleFormMixin, forms.ModelForm):
    """Форма профиля пользователя for manager"""

    class Meta:
        model = User
        fields = ['is_active']


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
