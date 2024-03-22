from django import forms

from config.utils.mixins import StyleFormMixin
from distribution.models import Client


class ClientForm(StyleFormMixin, forms.ModelForm):
    """ Form for creating a new client or updating an"""
    class Meta:
        model = Client
        exclude = ['owner', 'comment']

