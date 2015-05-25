# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('',
    # REST api views:
    # url(r'^list/(?P<slug>[\w-]+)/(?P<pk>\d+)/', BasicPollView.as_view(), name='list_entry'),
    # url(r'^list/(?P<slug>[\w-]+)/', BasicPollView.as_view(), name='list'),
    # url(r'^list/', BasicPollView.as_view(), name='list_default'),
    url(r'^delete/(?P<pk>\d+)', delete_poll, name='delete'),
    # Static views:
    url(r'^details/(?P<pk>\d+)', PollDetails.as_view(), name='details'),
    url(r'^results/(?P<pk>\d+)', PollResults.as_view(), name='results'),
    url(r'^verify/(?P<pk>\d+)', save_answers, name='verify'),
    url(r'(?P<location_slug>[\w-]+)/(?P<pk>\d+)/update/', PollUpdateView.as_view(), name='update'),
    url(r'(?P<slug>[\w-]+)/', SimplePollTakeView.as_view(), name='test'),
)
