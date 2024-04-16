from django.urls import path

from distribution.apps import DistributionConfig
from distribution.views import MailingEventListView, MailingEventCreateView, MailingEventUpdateView, \
    MailingEventDeleteView, MailingEventDetailView, ClientListView, ClientDetailView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView

app_name = DistributionConfig.name

urlpatterns = [
    path('event_list/', MailingEventListView.as_view(), name='mailing_event_list'),
    path('event_detail/<int:pk>/', MailingEventDetailView.as_view(), name='mailing_event_detail'),
    path('event_create', MailingEventCreateView.as_view(), name='mailing_event_create'),
    path('event_update/<int:pk>/', MailingEventUpdateView.as_view(), name='mailing_event_update'),
    path('event_delete/<int:pk>/', MailingEventDeleteView.as_view(), name='mailing_event_delete'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
