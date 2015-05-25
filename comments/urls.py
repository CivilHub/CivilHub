# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from comments.views import *

from rest.routers import HybridRouter

import api

router = HybridRouter()
router.register('list', api.CommentList, 'list')
router.add_api_view('answers', url(r'^answers/', api.CommentAnswers.as_view(),
                                   name='answers'))

urlpatterns = patterns('',
    url('^count/(?P<object_id>\d+)/(?P<app_label>.+)/(?P<model_label>.+)/$', get_comment_count, name='count'),
    url('^tree/(?P<object_id>\d+)/(?P<app_label>.+)/(?P<model_label>.+)/$', get_comment_tree, name='tree'),
)
