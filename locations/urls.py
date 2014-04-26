# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from locations.views import *

urlpatterns = patterns('',
    url(r'^$', LocationListView.as_view(), name='index'),
    url(r'details/(?P<pk>\d+)', LocationDetailView.as_view(), name='details'),
    url(r'create', CreateLocationView.as_view(), name='create'),
    url(r'delete/(?P<pk>\d+)', DeleteLocationView.as_view(), name='delete'),
    url(r'update/(?P<pk>\d+)', UpdateLocationView.as_view(), name='update'),
)
