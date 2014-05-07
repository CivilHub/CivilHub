# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import *

urlpatterns = patterns('',
    url(r'^/$', IdeasListView.as_view(), name='index'),
    url(r'vote/', vote, name='vote'),
    url(r'create/', CreateIdeaView.as_view(), name='create'),
    url(r'details/(?P<pk>\d+)', IdeasDetailView.as_view(), name='details'),
    url(r'delete/(?P<pk>\d+)', DeleteIdeaView.as_view(), name='delete'),
    url(r'update/(?P<pk>\d+)', UpdateIdeaView.as_view(), name='update'),
)
