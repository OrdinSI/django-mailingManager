from django.shortcuts import render
from django.views.generic import ListView


class HomeListView(ListView):
    """ Представление для домашней страницы"""
    template_name = 'home/home.html'

    def get_queryset(self):
        return



