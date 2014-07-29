# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

# mobile API
from rest_framework import routers
router = routers.DefaultRouter()
router.register('entries', NewsAPIView, 'entries')

urlpatterns = patterns('',
    # Get single news entry in JSON format
    url(r'list/(?P<slug>[\w-]+)/(?P<pk>\d+)/', BasicBlogView.as_view(), name='list_entry'),
    # Get all entries for selected location
    url(r'list/(?P<slug>[\w-]+)/', BasicBlogView.as_view(), name='list'),
    # Get all entries from blog application
    url(r'list/', BasicBlogView.as_view(), name='list_default'),
    # Static views (mostly unused)
    url(r'^$', NewsListView.as_view(), name='index'),
    url(r'^(?P<slug>[\w-]+)/update/', NewsUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)', NewsDetailView.as_view(), name='details'),
    url(r'^create', NewsCreateView.as_view(), name='new'),
    # Manage blog categories
    url(r'^category/(?P<slug>[\w-]+)', CategoryDetailView.as_view(), name='category'),
    url(r'categories/create', CategoryCreateView.as_view(), name='newcategory'),
    url(r'categories/', CategoryListView.as_view(), name='categories'),
)