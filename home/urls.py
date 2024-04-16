from django.views.decorators.cache import cache_page

from home.apps import HomeConfig
from django.urls import path

from home.views import HomeView

app_name = HomeConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
