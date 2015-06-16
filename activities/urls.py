# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest.routers import HybridRouter

import api
import views

router = HybridRouter()

router.register('actstream', api.ActivityViewSet, 'actstream')
router.add_api_view('follow', url(r'^follow/', api.FollowObjectView.as_view(), name='follow'))
router.add_api_view('follow-all', url(r'^follow-all/', api.FollowAllAPIView.as_view(), name='follow-all'))
router.add_api_view('action-graph', url(r'^action-graph/', api.ActionGraphAPIView.as_view(), name='action-graph'))

urlpatterns = patterns('',
    url(r'^followed/(?P<username>[\w-]+)/', views.FollowedUserList.as_view(), name='followed'),
    url(r'^facebook-friends/(?P<username>[\w-]+)/', views.FacebookFriendList.as_view(), name='facebook-friends'),
)
