# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from .views import *


urlpatterns = patterns('',
    # Wordpress-like media uploader
    url(r'^image/(?P<pk>\d+)/', ImageView.as_view(), name='image'),
    url(r'^(?P<filename>.*\w+)', UserGalleryView.as_view(), name='gallery_delete'),
    url(r'^$', UserGalleryView.as_view(), name='index'),
)
