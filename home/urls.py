from home.apps import HomeConfig
from django.urls import path

from home.views import HomeListView

app_name = HomeConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
]