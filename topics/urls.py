# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from topics.views import *

urlpatterns = patterns('',
    url('^(?P<slug>[\w-]+)/', DiscussionDetailView.as_view(), name='details'),
    url('^$', index_view, name='index'),
)
