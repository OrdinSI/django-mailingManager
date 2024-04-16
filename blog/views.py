from django.shortcuts import render
from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    """Blog detail view."""
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object

