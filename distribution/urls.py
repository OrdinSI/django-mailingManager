from django.urls import path

from distribution.apps import DistributionConfig
from distribution.views import MailingEventListView

app_name = DistributionConfig.name

urlpatterns = [
    path('', MailingEventListView.as_view(), name='mailingevent_list'),
]
