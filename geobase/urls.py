# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

from rest import routers
router = routers.HybridRouter()
router.register('countries', views.CountryAPIViewSet, 'countries')
router.register('codes', views.CountryCodeAPIViewSet, 'codes')
router.add_api_view('geoip', url(r'^geoip/(?P<ip>((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9]))/$', views.GeolocationAPIView.as_view(), name='geoip'))
router.add_api_view('geoip', url(r'^geoip/$', views.GeolocationAPIView.as_view(), name='geoip'))

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
)