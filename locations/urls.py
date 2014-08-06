# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from ideas.views import IdeasDetailView
from blog.views import NewsDetailView
from topics.views import DiscussionDetailView
from polls.views import PollDetails, PollResults
from gallery.views import PlaceGalleryView, PlacePictureView
from locations.views import *
from staticpages.views import PageView

from rest_framework import routers
router = routers.DefaultRouter()
router.register('locations', LocationAPIViewSet, 'locations')
router.register('markers', LocationMapViewSet, 'markers')

urlpatterns = patterns('',
    url(r'^places/', LocationListView.as_view(), name='index'),
    url(r'^(?P<slug>[\w-]+)/$', LocationDetailView.as_view(), name='details'),
    # lista sub-lokalizacji
    url(r'^(?P<slug>[\w-]+)/sublocations/$', SublocationList.as_view(), name='sublocations'),
    # wyszukiwanie treści w/g tagów
    url(r'^(?P<slug>[\w-]+)/search/(?P<tag>[\w-]+)$', LocationContentSearch.as_view(), name='tag_search'),
    url(r'^(?P<slug>[\w-]+)/search/$', LocationContentSearch.as_view(), name='tag_search_index'),
    # wyszukiwanie treści w/g kategorii
    url(r'^(?P<slug>[\w-]+)/filter/(?P<app>[\w-]+)/(?P<model>[\w-]+)/(?P<category>\d+)/$', LocationContentFilter.as_view(), name='category_search'),
    # Location ideas sub-views
    url(r'^(?P<slug>[\w-]+)/ideas/create', LocationIdeaCreate.as_view(), name='new_idea'),
    url(r'^(?P<place_slug>[\w-]+)/ideas/(?P<slug>[\w-]+)', IdeasDetailView.as_view(), name='idea_detail'),
    url(r'^(?P<slug>[\w-]+)/ideas', LocationIdeasList.as_view(), name='ideas'),
    # Location news entries sub-views
    url(r'^(?P<slug>[\w-]+)/news/create', LocationNewsCreate.as_view(), name='news_create'),
    url(r'^(?P<place_slug>[\w-]+)/news/(?P<slug>[\w-]+)', NewsDetailView.as_view(), name='news_detail'),
    url(r'^(?P<slug>[\w-]+)/news/', LocationNewsList.as_view(), name='news'),
    # Location forum (discussions)
    url(r'^(?P<slug>[\w-]+)/discussion/create/', LocationDiscussionCreate.as_view(), name='new_topic'),
    url(r'^(?P<place_slug>[\w-]+)/discussion/(?P<slug>[\w-]+)/', DiscussionDetailView.as_view(), name='topic'),
    url(r'^(?P<slug>[\w-]+)/discussion/', LocationDiscussionsList.as_view(), name='discussions'),
    url(r'^(?P<slug>[\w-]+)/discussions/', ajax_discussion_list, name='ajaxlist'),
    #url(r'^(?P<slug>[\w-]+)/discussions/(?P<limit>[\w-]+)/', location_discussion_list, name='dsublist'),
    # Location polls (create, edit, delete etc. just for this location)
    url(r'^(?P<slug>[\w-]+)/polls/create/', LocationPollCreate.as_view(), name='new_poll'),
    url(r'^(?P<place_slug>[\w-]+)/polls/(?P<slug>[\w-]+)/results/', PollResults.as_view(), name='results'),
    url(r'^(?P<place_slug>[\w-]+)/polls/(?P<slug>[\w-]+)', PollDetails.as_view(), name='poll'),
    url(r'^(?P<slug>[\w-]+)/polls/', LocationPollsList.as_view(), name='polls'),
    # Location followers list
    url(r'^(?P<slug>[\w-]+)/followers/', LocationFollowersList.as_view(), name='followers'),
    # Location media gallery
    url(r'^(?P<slug>[\w-]+)/gallery/(?P<pk>\d+)/', PlacePictureView.as_view(), name='picture'),
    url(r'^(?P<slug>[\w-]+)/gallery/', PlaceGalleryView.as_view(), name='gallery'),
    # Generic location views
    url(r'create', CreateLocationView.as_view(), name='create'),
    url(r'delete/(?P<slug>[\w-]+)/', DeleteLocationView.as_view(), name='delete'),
    url(r'update/(?P<slug>[\w-]+)/', UpdateLocationView.as_view(), name='update'),
    # Ajaxy functions - follow/unfollow location actions
    url(r'add_follower/(?P<pk>\d+)', add_follower, name='add_follower'),
    url(r'remove_follower/(?P<pk>\d+)', remove_follower, name='remove_follower'),
    url(r'background/(?P<pk>\d+)', change_background, name='background'),
    # Ajaxy functions - invite other users to follow location.
    url(r'invite_users/(?P<pk>\d+)', InviteUsersView.as_view(), name='invite')
)
