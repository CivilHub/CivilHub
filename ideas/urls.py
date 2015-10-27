# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import *
import api

from rest.routers import HybridRouter
router = HybridRouter()
router.register('categories', api.IdeaCategoryViewSet, 'idea-categories')
router.register('ideas', api.IdeaViewSet, 'ideas')
router.register('votes', api.IdeaVoteViewSet, 'votes')

urlpatterns = patterns('',
    url(r'categories/create/', CreateCategory.as_view(), name='new_category'),
    url(r'vote-form/(?P<pk>[\d]+)/(?P<status>[\d]+)/', VoteCommentFormView.as_view(), name='vote-form'),
    url(r'create/', CreateIdeaView.as_view(), name='create'),
    url(r'details/(?P<slug>[\w-]+)', IdeasDetailView.as_view(), name='details'),
    url(r'update/(?P<slug>[\w-]+)', UpdateIdeaView.as_view(), name='update'),
    url(r'(?P<slug>[\w-]+)/gallery/upload/', PictureUploadView.as_view(), name='picture-upload'),
)
