# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.InviteToContentView.as_view(), name='invite'),
    url(r'^followers/(?P<pk>\d+)/', views.ComposeFollowersMessage.as_view(), name='followers-message'),
)
