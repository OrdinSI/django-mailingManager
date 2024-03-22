from django.contrib import admin

from distribution.models import Client, MailingEvent, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'owner')


@admin.register(MailingEvent)
class MailingEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'start_time', 'end_time')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing_event', 'subject', 'body')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'owner', 'attempt_time', 'status', 'response')
