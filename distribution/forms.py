from django import forms

from config.utils.mixins import StyleFormMixin
from config.utils.time_utils import convert_to_utc, convert_to_local_time
from distribution.models import Client, MailingEvent, Message
from distribution.tasks import schedule_email_task


class ClientForm(StyleFormMixin, forms.ModelForm):
    """ Form for creating a new client or updating an"""

    class Meta:
        model = Client
        exclude = ['owner']


class MailingEventForm(StyleFormMixin, forms.ModelForm):
    """ Form for creating a new mailing or updating an event"""

    subject = forms.CharField(max_length=255, label='Тема')
    body = forms.CharField(widget=forms.Textarea, label='Сообщение')

    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'], label='Начало рассылки')

    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'], label='Окончание рассылки')

    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label='Клиенты'
    )

    class Meta:
        model = MailingEvent
        exclude = ['owner', 'status', 'is_active']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user:
            self.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)

        if self.instance and hasattr(self.instance, 'message'):
            self.fields['subject'].initial = self.instance.message.subject
            self.fields['body'].initial = self.instance.message.body

        # if self.instance and self.instance.start_time:
        #     user_timezone = self.request.user.timezone
        #     local_start_time = convert_to_local_time(self.instance.start_time, user_timezone)
        #     local_end_time = convert_to_local_time(self.instance.end_time, user_timezone)
        #
        #     self.fields['start_time'].initial = local_start_time
        #     self.fields['end_time'].initial = local_end_time


    def save(self, commit=True):
        mailing_event = super().save(commit=False)
        mailing_event.owner = self.request.user

        user_timezone = self.request.user.timezone

        mailing_event.start_time = convert_to_utc(self.cleaned_data['start_time'], user_timezone)
        mailing_event.end_time = convert_to_utc(self.cleaned_data['end_time'], user_timezone)

        if commit:
            mailing_event.save()
            self.save_m2m()
            schedule_email_task(mailing_event)

        message, created = Message.objects.get_or_create(mailing_event=mailing_event)
        message.subject = self.cleaned_data['subject']
        message.body = self.cleaned_data['body']
        if commit:
            message.save()
        return mailing_event


class MessageForm(StyleFormMixin, forms.ModelForm):
    """ Form for creating a new mailing or updating an"""

    class Meta:
        model = Message
        fields = ['subject', 'body']
