# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from locations.views import *

urlpatterns = patterns('',
    url(r'^$', LocationListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)$', LocationDetailView.as_view(), name='details'),
    url(r'^news/(?P<pk>\d+)', LocationNewsList.as_view(), name='news'),
    url(r'^ideas/(?P<pk>\d+)', LocationIdeasList.as_view(), name='ideas'),
    url(r'^followers/(?P<pk>\d+)', LocationFollowersList.as_view(), name='followers'),
    url(r'create', CreateLocationView.as_view(), name='create'),
    url(r'delete/(?P<pk>\d+)', DeleteLocationView.as_view(), name='delete'),
    url(r'update/(?P<pk>\d+)', UpdateLocationView.as_view(), name='update'),
    url(r'add_follower/(?P<pk>\d+)', add_follower, name='add_follower'),
    url(r'remove_follower/(?P<pk>\d+)', remove_follower, name='remove_follower'),
)
