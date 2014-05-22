# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('',
    url(r'^details/(?P<pk>\d+)', PollDetails.as_view(), name='details'),
    url(r'^verify/(?P<pk>\d+)', save_answers, name='verify'),
    url(r'^delete/(?P<pk>\d+)', delete_poll, name='delete'),
)
