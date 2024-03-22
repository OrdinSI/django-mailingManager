from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from distribution.forms import ClientForm
from distribution.models import MailingEvent, Client


class MailingEventListView(ListView):
    """ View for listing all mailing events """
    model = MailingEvent


class MailingEventDetailView(DetailView):
    """ View for detail mailing event """
    model = MailingEvent


class MailingEventCreateView(CreateView):
    """ View for creating new mailing event """
    model = MailingEvent


class MailingEventUpdateView(UpdateView):
    """ View for updating existing mailing event """
    model = MailingEvent


class MailingEventDeleteView(DeleteView):
    """ View for deleting existing mailing event"""
    model = MailingEvent


class ClientListView(LoginRequiredMixin, ListView):
    """ View for listing all clients """
    model = Client
    login_url = 'home:home'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ View for detail client"""
    model = Client
    login_url = 'home:home'


class ClientCreateView(LoginRequiredMixin,  CreateView):
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
    login_url = 'home:home'


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ View for deleting existing client"""
    model = Client
    login_url = 'home:home'
