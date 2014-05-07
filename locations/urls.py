# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from locations.views import *

urlpatterns = patterns('',
    url(r'^$', LocationListView.as_view(), name='index'),
    url(r'^(?P<slug>\w+)/$', LocationDetailView.as_view(), name='details'),
    url(r'^(?P<slug>\w+)/news/', LocationNewsList.as_view(), name='news'),
    url(r'^(?P<slug>\w+)/ideas/', LocationIdeasList.as_view(), name='ideas'),
    url(r'^(?P<slug>\w+)/followers/', LocationFollowersList.as_view(), name='followers'),
    url(r'create', CreateLocationView.as_view(), name='create'),
    url(r'delete/(?P<slug>\w+)/', DeleteLocationView.as_view(), name='delete'),
    url(r'update/(?P<slug>\w+)/', UpdateLocationView.as_view(), name='update'),
    url(r'add_follower/(?P<pk>\d+)', add_follower, name='add_follower'),
    url(r'remove_follower/(?P<pk>\d+)', remove_follower, name='remove_follower'),
)
