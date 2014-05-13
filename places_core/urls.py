# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from places_core.views import CreateAbuseReport, report_sent


urlpatterns = patterns('',
    url(r'^sent/', report_sent),
    url(r'^(?P<app_label>.+)/(?P<model_label>.+)/(?P<object_pk>\d+)/', CreateAbuseReport.as_view()),
)
