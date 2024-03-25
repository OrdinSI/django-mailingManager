from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from distribution.forms import ClientForm, MailingEventForm
from distribution.models import MailingEvent, Client


class MailingEventListView(LoginRequiredMixin, ListView):
    """ View for listing all mailing events """
    model = MailingEvent
    login_url = 'home:home'

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        queryset = queryset.select_related('message')
        return queryset


class MailingEventDetailView(LoginRequiredMixin, DetailView):
    """ View for detail mailing event """
    model = MailingEvent
    login_url = 'home:home'


class MailingEventCreateView(LoginRequiredMixin, CreateView):
    """ View for creating new mailing event """
    model = MailingEvent
    form_class = MailingEventForm
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:mailing_event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        field_order = ['subject', 'body', 'start_time', 'end_time', 'frequency', 'clients']
        context['field_order'] = [form[field] for field in field_order if field in form.fields]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class MailingEventUpdateView(LoginRequiredMixin, UpdateView):
    """ View for updating existing mailing event """
    model = MailingEvent
    form_class = MailingEventForm
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:mailing_event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        field_order = ['subject', 'body', 'start_time', 'end_time', 'frequency', 'clients']
        context['field_order'] = [form[field] for field in field_order if field in form.fields]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class MailingEventDeleteView(LoginRequiredMixin, DeleteView):
    """ View for deleting existing mailing event"""
    model = MailingEvent
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:mailing_event_list')


class ClientListView(LoginRequiredMixin, ListView):
    """ View for listing all clients """
    model = Client
    login_url = 'home:home'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ View for detail client"""
    model = Client
    login_url = 'home:home'


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ View for creating new client"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:client_list')
    login_url = 'home:home'

    def form_valid(self, form):
        client = form.save(commit=False)
        client.owner = self.request.user
        client.save()

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ View for updating existing client"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:client_list')
    login_url = 'home:home'


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ View for deleting existing client"""
    model = Client
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:client_list')
