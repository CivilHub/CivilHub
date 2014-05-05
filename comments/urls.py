# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from comments.views import *

urlpatterns = patterns('',
    url('^count/(?P<object_id>\d+)/(?P<app_label>.+)/(?P<model_label>.+)/$', get_comment_count, name='count'),
    url('^tree/(?P<object_id>\d+)/(?P<app_label>.+)/(?P<model_label>.+)/$', get_comment_tree, name='tree'),
)
