# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from django.utils.translation import get_language
import views


urlpatterns = patterns('',
    url(r'^(?P<page>[\w-]+)/$', views.PageView.as_view(), name='page'),
    url(r'^$', cache_page(60*60, key_prefix='home_'+get_language())(views.PageView.as_view()), name='page'),
)
