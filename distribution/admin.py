from django.contrib import admin

from distribution.models import Client, MailingEvent, MailingSetting, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')


@admin.register(MailingEvent)
class MailingEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'send_time', 'setting')


@admin.register(MailingSetting)
class MailingSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'frequency', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_event', 'subject', 'body')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'user', 'attempt_time', 'status', 'response')
