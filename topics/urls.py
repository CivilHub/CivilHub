# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from topics.views import *

urlpatterns = patterns('',
    url('^$', index_view, name='index'),
)
