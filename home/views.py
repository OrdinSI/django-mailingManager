from django.shortcuts import render
from django.views.generic import View
from blog.models import Blog
from distribution.models import MailingEvent, Client
from home.services import get_post


class HomeView(View):
    """ Представление для домашней страницы"""
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        total_mailing_events = MailingEvent.objects.count()
        total_clients = Client.objects.count()
        active_mailing_events = MailingEvent.objects.filter(is_active=True).count()

        random_posts = get_post(Blog, 'random_posts')

        context = {
            'total_mailing_events': total_mailing_events,
            'total_clients': total_clients,
            'active_mailing_events': active_mailing_events,
            'random_posts': random_posts
        }
        return render(request, self.template_name, context)
