# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^create/', views.BlogEntryCreateView.as_view(), name="create"),
    url(r'^(?P<slug>[\w-]+)/update', views.BlogEntryUpdateView.as_view(), name="update"),
    url(r'^(?P<slug>[\w-]+)/', views.BlogEntryDetailView.as_view(), name="detail"),
)
