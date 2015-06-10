# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest.routers import HybridRouter

import api
from .views import *

router = HybridRouter()
router.add_api_view('answers', url(r'^answers/', api.AnswerSetAPIView.as_view(), name='answers'))
router.add_api_view('timeline', url(r'^timeline/', api.AnswersInTimeAPIView.as_view(), name='timeline'))

urlpatterns = patterns('',
    url(r'^delete/(?P<pk>\d+)', delete_poll, name='delete'),
    url(r'^details/(?P<pk>\d+)', PollDetails.as_view(), name='details'),
    url(r'^results/(?P<pk>\d+)', PollResults.as_view(), name='results'),
    url(r'^verify/(?P<pk>\d+)', save_answers, name='verify'),
    url(r'(?P<location_slug>[\w-]+)/(?P<pk>\d+)/update/', PollUpdateView.as_view(), name='update'),
    url(r'(?P<slug>[\w-]+)/', SimplePollTakeView.as_view(), name='test'),
)
