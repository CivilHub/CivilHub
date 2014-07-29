# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from topics.views import *

# mobile API
from rest_framework import routers
router = routers.DefaultRouter()
router.register('topic', ForumTopicAPIViewSet, 'topic')
router.register('entry', ForumEntryAPIViewSet, 'entry')

urlpatterns = patterns('',
    url('^delete/', delete_topic, name='delete'),
    url('^(?P<slug>[\w-]+)/reply/', reply, name='reply'),
    url('^(?P<slug>[\w-]+)/update/', DiscussionUpdateView.as_view(), name='update'),
    url('^(?P<slug>[\w-]+)/list/', DiscussionListView.as_view(), name='list'),
    url('^(?P<pk>\d+)/vote/', vote, name='vote'),
    url('^(?P<slug>[\w-]+)/entry/(?P<pk>\d+)/update/', EntryUpdateView.as_view(), name='entry_update'),
    url('^(?P<pk>\d+)/delete/', DeleteDiscussionView.as_view(), name='remove'),
    url('^(?P<slug>[\w-]+)/', DiscussionDetailView.as_view(), name='details'),
)
