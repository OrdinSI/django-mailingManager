from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings


class User(AbstractUser):
    """Model definition for users in the system """
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **settings.NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **settings.NULLABLE)
    timezone = models.CharField(max_length=50, verbose_name='часовой пояс', default='UTC')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.phone}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
