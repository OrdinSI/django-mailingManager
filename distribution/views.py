from django.shortcuts import render
from django.views.generic import ListView
from distribution.models import MailingEvent


class MailingEventListView(ListView):
    model = MailingEvent


