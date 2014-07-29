# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import *

from rest_framework import routers
router = routers.DefaultRouter()
router.register('idea', IdeaAPIViewSet, 'ideas')

urlpatterns = patterns('',
    url(r'categories/create/', CreateCategory.as_view(), name='new_category'),
    url(r'^$', IdeasListView.as_view(), name='index'),
    url(r'vote/', vote, name='vote'),
    url(r'create/', CreateIdeaView.as_view(), name='create'),
    url(r'list/(?P<slug>[\w-]+)/', BasicIdeaView.as_view(), name='list'),
    url(r'list/', BasicIdeaView.as_view(), name='list_default'),
    url(r'details/(?P<slug>[\w-]+)', IdeasDetailView.as_view(), name='details'),
    url(r'delete/(?P<slug>[\w-]+)', DeleteIdeaView.as_view(), name='delete'),
    url(r'update/(?P<slug>[\w-]+)', UpdateIdeaView.as_view(), name='update'),
)
