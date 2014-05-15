# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('',
    url(r'^details/(?P<pk>\d+)', delete_poll, name='details'),
    url(r'^delete/(?P<pk>\d+)', delete_poll, name='delete'),
)
