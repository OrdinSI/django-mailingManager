from datetime import datetime, timedelta, timezone

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, View, UpdateView
from jose import jwt, JWTError

from config import settings
from users.forms import UserAuthenticationForm, UserRegisterForm, UserProfileForm, UserPasswordResetForm, \
    UserSetNewPasswordForm
from users.models import User


class UserLoginView(LoginView):
    """ Представление для аутентификации пользователя"""
    model = User
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'


class UserRegisterView(SuccessMessageMixin, CreateView):
    """ Представление для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home:home')
    success_message = ("На ваш адрес электронной почты было отправлено письмо с подтверждением. "
                       "Пожалуйста, проверьте свою электронную почту и нажмите на ссылку подтверждения, "
                       "чтобы завершить регистрацию. Если письмо не пришло, проверьте папку спам.")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        payload = {
            'sub': uid,
            'exp': datetime.now(timezone.utc) + timedelta(seconds=86400)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        activation_url = reverse('users:confirm_email', kwargs={'token': token})

        send_mail(
            subject='Подтвердите свой электронный адрес.',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:'
                    f'{settings.BASE_URL}{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class UserConfirmEmailView(View):
    """ Представление для обработки перехода по email пользователя"""

    success_url = reverse_lazy('home:home')
    error_message = ('Ссылка для подтверждения по электронной почте недействительна или срок ее действия истек. '
                     'Пожалуйста, зарегистрируйтесь снова.')

    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            uid_data = payload.get('sub')
            uid = urlsafe_base64_decode(uid_data)
            user = User.objects.get(pk=uid)
            if payload.get('exp') < datetime.now(timezone.utc).timestamp():
                self.error_message = 'Срок действия ссылки истек. Пожалуйста, зарегистрируйтесь снова.'
                messages.error(request, self.error_message)
                return redirect(self.success_url)

        except (jwt.ExpiredSignatureError, JWTError, User.DoesNotExist):
            messages.error(request, self.error_message)
            return redirect(self.success_url)

        user.is_active = True
        user.save()
        login(request, user)
        success_message = 'Ваш адрес электронной почты успешно подтвержден. Спасибо за регистрацию!'
        messages.success(request, success_message)
        return redirect(self.success_url)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """ Представление для профиля пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('home:home')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """ Представление для восстановления пароля"""
    model = User
    form_class = UserPasswordResetForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('home:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_email.html'


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Представление для ввода нового пароля"""
    model = User
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
