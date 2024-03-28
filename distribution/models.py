from django.db import models

from config import settings
from users.models import User


class Client(models.Model):
    """Model for clients"""
    first_name = models.CharField(max_length=255, verbose_name="имя")
    last_name = models.CharField(max_length=255, verbose_name="фамилия")
    email = models.EmailField(unique=True, verbose_name="email")
    comment = models.TextField(verbose_name="комментарий", **settings.NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата изменения")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.email}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class MailingEvent(models.Model):
    """Mailing Event model"""
    start_time = models.DateTimeField(verbose_name="время начала рассылки")
    end_time = models.DateTimeField(verbose_name="время окончания рассылки", **settings.NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата изменения")
    frequency = models.CharField(max_length=20,
                                 choices=[('once', 'Однократно'), ('daily', 'Ежедневно'), ('weekly', 'Еженедельно'),
                                          ('monthly', 'Ежемесячно')],
                                 verbose_name="периодичность")
    status = models.CharField(max_length=20,
                              choices=[('created', 'Создано'), ('started', 'Начато'), ('completed', 'Завершено')],
                              default='created',
                              verbose_name="статус")
    is_active = models.BooleanField(default=True, verbose_name='Активация рассылки')
    clients = models.ManyToManyField(Client, verbose_name="клиенты", related_name="mailing_events")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")

    def __str__(self):
        return f"{self.owner} {self.start_time}"

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"


class Message(models.Model):
    """Message Model"""
    mailing_event = models.OneToOneField(MailingEvent, on_delete=models.CASCADE, verbose_name="рассылка")
    subject = models.CharField(max_length=255, verbose_name="тема письма")
    body = models.TextField(verbose_name="тело письма")

    def __str__(self):
        return f"{self.mailing_event}, {self.subject}, {self.body}"

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"


class Log(models.Model):
    """Log model"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="дата попытки")
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')],
                              verbose_name="статус")
    response = models.TextField(verbose_name="ответ", **settings.NULLABLE)

    def __str__(self):
        return f"{self.message} - {self.owner}, {self.attempt_time}, {self.status}, {self.response}"

    class Meta:
        verbose_name = "лог"
        verbose_name_plural = "логи"
