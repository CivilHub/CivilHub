# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'^$', NewsListView.as_view(), name='index'),
    url(r'^(?P<slug>[\w-]+)', NewsDetailView.as_view(), name='details'),
    url(r'^create', NewsCreateView.as_view(), name='new'),
    url(r'^category/(?P<slug>[\w-]+)', CategoryDetailView.as_view(), name='category'),
    url(r'categories/create', CategoryCreateView.as_view(), name='newcategory'),
    url(r'categories/', CategoryListView.as_view(), name='categories'),
)