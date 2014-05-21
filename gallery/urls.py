# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from .views import test_view, UserGalleryView


urlpatterns = patterns('',
    # Wordpress-like media uploader
    url(r'^upload/', test_view, name='test'),
    url(r'^(?P<filename>.*\w+)', UserGalleryView.as_view(), name='gallery_delete'),
    url(r'^$', UserGalleryView.as_view(), name='index'),
)
