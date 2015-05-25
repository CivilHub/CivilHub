# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework import routers

import api
import views


router = routers.DefaultRouter()
router.register('content_types', api.ContentTypeAPIViewSet, 'content_types')
router.register('search', api.SearchResultsAPIViewSet, 'search')


urlpatterns = patterns('',
    url(r'^search/', views.CivilSearchView.as_view(), name="search-record"),
    url(r'^(?P<app_label>.+)/(?P<model_label>.+)/(?P<object_pk>\d+)/',
        views.CreateAbuseReport.as_view(), name='report'),
   	url(r'^(?P<ct>\d+)/(?P<pk>\d+)/', views.ReportView.as_view(), name="abuse-report"),
)
