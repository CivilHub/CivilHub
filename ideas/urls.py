# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import *
import api

from rest_framework import routers
router = routers.DefaultRouter()
router.register('idea', api.IdeaAPIViewSet, 'ideas')
router.register('categories', api.IdeaCategoryAPIViewSet, 'categories')
router.register('votes', api.IdeaVoteAPIViewSet, 'votes')

urlpatterns = patterns('',
    url(r'categories/create/', CreateCategory.as_view(), name='new_category'),
    #url(r'^$', IdeasListView.as_view(), name='index'),
    url(r'vote/(?P<pk>\d+)/', IdeaVotesView.as_view(), name='vote'),
    url(r'create/', CreateIdeaView.as_view(), name='create'),
    url(r'details/(?P<slug>[\w-]+)', IdeasDetailView.as_view(), name='details'),
    url(r'update/(?P<slug>[\w-]+)', UpdateIdeaView.as_view(), name='update'),
    url(r'(?P<slug>[\w-]+)/gallery/upload/', PictureUploadView.as_view(), name='picture-upload'),
)
