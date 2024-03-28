
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from config.utils.time_utils import convert_to_local_time
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

    def get_context_data(self, **kwargs):
        context = super(MailingEventDetailView, self).get_context_data(**kwargs)
        event = context['object']
        user_timezone = self.request.user.timezone

        if event.start_time:
            context['start_time'] = (convert_to_local_time(event.start_time, user_timezone)).strftime("%Y-%m-%d %H:%M")
        if event.end_time:
            context['end_time'] = (convert_to_local_time(event.end_time, user_timezone)).strftime("%Y-%m-%d %H:%M")

        return context


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

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        user_timezone = self.request.user.timezone
        if obj.start_time:
            initial['start_time'] = convert_to_local_time(obj.start_time, user_timezone)
        if obj.end_time:
            initial['end_time'] = convert_to_local_time(obj.end_time, user_timezone)
        return initial


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
