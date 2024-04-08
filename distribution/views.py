from collections import defaultdict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from distribution.forms import ClientForm, MailingEventForm, ManagerMailingEventForm
from distribution.models import MailingEvent, Client
from utils.time_utils import convert_to_local_time


class MailingEventListView(LoginRequiredMixin, ListView):
    """ View for listing all mailing events """
    model = MailingEvent
    login_url = 'users:login'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('message')
        if self.request.user.is_superuser or self.request.user.has_perm('distribution.set_is_active_event'):
            return queryset
        else:
            return queryset.filter(owner=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_create_button'] = not self.request.user.groups.filter(name='manager').exists()
        if self.request.user.is_superuser or self.request.user.has_perm('distribution.set_is_active_event'):
            context['user_type'] = 'admin_manager'
            mailing_events_by_owner = defaultdict(list)
            for mailing_event in context['object_list']:
                mailing_events_by_owner[mailing_event.owner].append(mailing_event)
            context['mailing_events_by_owner'] = dict(mailing_events_by_owner)
            return context
        else:
            return context


class MailingEventDetailView(LoginRequiredMixin, DetailView):
    """ View for detail mailing event """
    model = MailingEvent
    login_url = 'home:home'

    def get_context_data(self, **kwargs):
        context = super(MailingEventDetailView, self).get_context_data(**kwargs)
        event = context['object']
        user_timezone = self.request.user.timezone
        context['show_create_button'] = not self.request.user.groups.filter(name='manager').exists()

        if event.start_time:
            context['start_time'] = (convert_to_local_time(event.start_time, user_timezone)).strftime("%Y-%m-%d %H:%M")
        if event.end_time:
            context['end_time'] = (convert_to_local_time(event.end_time, user_timezone)).strftime("%Y-%m-%d %H:%M")

        return context


class MailingEventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """ View for creating new mailing event """
    model = MailingEvent
    form_class = MailingEventForm
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:mailing_event_list')

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()

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
        field_order = ['subject', 'body', 'start_time', 'end_time', 'frequency', 'clients', 'owner', 'is_active']
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

    def get_form_class(self):
        if self.request.user.has_perm('distribution.set_is_active_event') and not self.request.user.is_superuser:
            return ManagerMailingEventForm
        else:
            return MailingEventForm


class MailingEventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ View for deleting existing mailing event"""
    model = MailingEvent
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:mailing_event_list')

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()


class ClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """ View for listing all clients """
    model = Client
    login_url = 'users:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()


class ClientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """ View for detail client"""
    model = Client
    login_url = 'home:home'

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ View for updating existing client"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('distribution:client_list')
    login_url = 'home:home'

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ View for deleting existing client"""
    model = Client
    login_url = 'home:home'
    success_url = reverse_lazy('distribution:client_list')

    def test_func(self):
        return not self.request.user.groups.filter(name='manager').exists()
