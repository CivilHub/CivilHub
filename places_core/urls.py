# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest.routers import HybridRouter

import api
import views

router = HybridRouter()
router.register('content_types', api.ContentTypeAPIViewSet, 'content_types')
router.register('search', api.SearchResultsAPIViewSet, 'search')
router.add_api_view('resons', url(r'^reasons/', api.AbuseReasonList.as_view(), name='reasons'))


urlpatterns = patterns('',
    url(r'^search/', views.CivilSearchView.as_view(), name="search-record"),
    url(r'^(?P<app_label>.+)/(?P<model_label>.+)/(?P<object_pk>\d+)/',
        views.CreateAbuseReport.as_view(), name='report'),
   	url(r'^(?P<ct>\d+)/(?P<pk>\d+)/', views.ReportView.as_view(), name="abuse-report"),
)
