# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from .views import *

from rest.routers import HybridRouter
router = HybridRouter()
router.register(r'usermedia', UserGalleryAPIViewSet, 'usermedia')


urlpatterns = patterns('',
    # Wordpress-like media uploader
    url(r'^image/(?P<pk>\d+)/', ImageView.as_view(), name='image'),
    #url(r'^(?P<filename>.*\w+)', UserGalleryView.as_view(), name='gallery_delete'),
    url(r'^update/(?P<pk>\d+)/', UserGalleryUpdateView.as_view(), name='update'),
    url(r'^upload/', UserGalleryCreateView.as_view(), name='upload'),
    url(r'^(?P<username>[\w-]+)/', UserGalleryView.as_view(), name='user_gallery'),
    url(r'^$', UserGalleryView.as_view(), name='index'),
)
