# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from locations.views import LocationListView

urlpatterns = patterns('',
    url(r'^$', LocationListView.as_view(), name='index'),
)
