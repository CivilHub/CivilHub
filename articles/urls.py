# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^top-level-article/', views.TopLevelArticleView.as_view(article_slug='top-level-article'), name='top-level-article'),
    url(r'^blog/(?P<slug>[\w-]+)/', views.BlogEntryView.as_view(), name='blog_entry'),
    url(r'^blog/', views.BlogListView.as_view(), name='blog'),
    url(r'^support/(?P<slug>[\w-]+)/', views.SupportEntryView.as_view(), name='support_entry'),
    url(r'^support/', views.SupportListView.as_view(), name='support'),
)
