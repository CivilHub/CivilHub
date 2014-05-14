# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('',
    url(r'^category/create/', CreateCategoryView.as_view(), name='new_category'),
    url(r'^category/', CategoryList.as_view(), name='categories'),
    url(r'^verify/', verify_poll, name='verify'),
    url(r'^answer/(?P<pk>\d+)/', PollAnswerSet.as_view(), name='answer'),
    url(r'^delete/(?P<pk>\d+)/', delete_poll, name='delete'),
)
