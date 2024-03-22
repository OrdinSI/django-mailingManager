from django import forms

from config.utils.mixins import StyleFormMixin
from distribution.models import Client, MailingEvent


class ClientForm(StyleFormMixin, forms.ModelForm):
    """ Form for creating a new client or updating an"""

    class Meta:
        model = Client
        exclude = ['owner']


class MailingEventForm(StyleFormMixin, forms.ModelForm):
    """ Form for creating a new mailing or updating an event"""

    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'], label='Начало рассылки')

    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'], label='Окончание рассылки')

    class Meta:
        model = MailingEvent
        exclude = ['owner', 'status']
