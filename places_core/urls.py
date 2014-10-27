# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from places_core import views
# REST API
from rest_framework import routers
router = routers.DefaultRouter()
router.register('content_types', views.ContentTypeAPIViewSet, 'content_types')
router.register('search', views.SearchResultsAPIViewSet, 'search')


urlpatterns = patterns('',
    url(r'^test/', views.HelloPDFView.as_view(), name='pdf_test'),
    url(r'^sent/', views.report_sent),
    url(r'^(?P<app_label>.+)/(?P<model_label>.+)/(?P<object_pk>\d+)/',
        views.CreateAbuseReport.as_view(), name='report'),
)
