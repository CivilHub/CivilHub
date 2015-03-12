# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .api import NewsAPIView, BlogCategoryAPIViewSet
from views import *

# mobile API
from rest_framework import routers
router = routers.DefaultRouter()
router.register('entries', NewsAPIView, 'entries')
router.register('categories', BlogCategoryAPIViewSet, 'categories')

urlpatterns = patterns('',
    # url(r'^$', NewsListView.as_view(), name='index'),
    # url(r'^(?P<slug>[\w-]+)/update/', NewsUpdateView.as_view(), name='update'),
    # url(r'^(?P<slug>[\w-]+)', NewsDetailView.as_view(), name='details'),
    # url(r'^create', NewsCreateView.as_view(), name='new'),
    # url(r'^category/(?P<slug>[\w-]+)', CategoryDetailView.as_view(), name='category'),
    # url(r'categories/create', CategoryCreateView.as_view(), name='newcategory'),
    # url(r'categories/', CategoryListView.as_view(), name='categories'),
)