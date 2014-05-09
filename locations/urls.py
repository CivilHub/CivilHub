# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import IdeasDetailView
from blog.views import NewsDetailView
from locations.views import *

urlpatterns = patterns('',
    url(r'^$', LocationListView.as_view(), name='index'),
    url(r'^(?P<slug>[\w-]+)/$', LocationDetailView.as_view(), name='details'),
    # Location ideas sub-views
    url(r'^(?P<slug>[\w-]+)/ideas/create', LocationIdeaCreate.as_view(), name='new_idea'),
    url(r'^(?P<place_slug>[\w-]+)/ideas/(?P<slug>[\w-]+)', IdeasDetailView.as_view(), name='idea_detail'),
    url(r'^(?P<slug>[\w-]+)/ideas', LocationIdeasList.as_view(), name='ideas'),
    # Location news entries sub-views
    url(r'^(?P<slug>[\w-]+)/news/create', LocationNewsCreate.as_view(), name='news_create'),
    url(r'^(?P<place_slug>[\w-]+)/news/(?P<slug>[\w-]+)', NewsDetailView.as_view(), name='news_detail'),
    url(r'^(?P<slug>[\w-]+)/news/', LocationNewsList.as_view(), name='news'),
    # Location followers list
    url(r'^(?P<slug>[\w-]+)/followers/', LocationFollowersList.as_view(), name='followers'),
    # Generic location views
    url(r'create', CreateLocationView.as_view(), name='create'),
    url(r'delete/(?P<slug>[\w-]+)/', DeleteLocationView.as_view(), name='delete'),
    url(r'update/(?P<slug>[\w-]+)/', UpdateLocationView.as_view(), name='update'),
    # Ajaxy functions - follow/unfollow location actions
    url(r'add_follower/(?P<pk>\d+)', add_follower, name='add_follower'),
    url(r'remove_follower/(?P<pk>\d+)', remove_follower, name='remove_follower'),
)
