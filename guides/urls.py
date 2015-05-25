# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^create/(?P<location_slug>[\w-]+)/', views.GuideCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/delete-editor/', views.EditorDeleteView.as_view(), name='delete-editor'),
    url(r'^(?P<location_slug>[\w-]+)/by-tag/(?P<tag_pk>\d+)/', views.GuideTagFilteredListView.as_view(), name='list-filter-tag'),
    url(r'^(?P<location_slug>[\w-]+)/by-category/(?P<category_pk>\d+)/', views.GuideCategoryFilteredListView.as_view(), name='list-filter-category'),
    url(r'^(?P<location_slug>[\w-]+)/(?P<slug>[\w-]+)/delete/', views.GuideDeleteView.as_view(), name='delete'),
    url(r'^(?P<location_slug>[\w-]+)/(?P<slug>[\w-]+)/update/', views.GuideUpdateView.as_view(), name='update'),
    url(r'^(?P<location_slug>[\w-]+)/(?P<slug>[\w-]+)/editors/', views.GuideEditorsListView.as_view(), name='editors'),
    url(r'^(?P<location_slug>[\w-]+)/(?P<slug>[\w-]+)/', views.GuideDetailView.as_view(), name='detail'),
    url(r'^(?P<location_slug>[\w-]+)/', views.GuideListView.as_view(), name='list'),
)
