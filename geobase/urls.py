# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

from rest_framework import routers
router = routers.DefaultRouter()
router.register('countries', views.CountryAPIViewSet, 'countries')
router.register('codes', views.CountryCodeAPIViewSet, 'codes')

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
)