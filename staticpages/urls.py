# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^(?P<page>[\w-]+)/$', views.PageView.as_view(), name='page'),
    url(r'^$', views.PageView.as_view(), name='page'),
)
