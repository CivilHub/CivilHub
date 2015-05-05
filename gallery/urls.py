# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, url
from .views import *

from rest.routers import HybridRouter
router = HybridRouter()
router.register(r'usermedia', UserGalleryAPIViewSet, 'usermedia')


urlpatterns = patterns('',
    url(r'^albums/create/(?P<ct>\d+)/(?P<pk>\d+)/', GalleryCreateView.as_view(), name='album-create-for'),
    url(r'^albums/create/', GalleryCreateView.as_view(), name='album-create'),
    url(r'^albums/(?P<pk>\d+)/manage/', MassDeleteView.as_view(), name='mass-delete'),
    url(r'^albums/(?P<pk>\d+)/upload/', PictureUploadView.as_view(), name='picture-upload'),
    url(r'^albums/(?P<pk>\d+)/delete/', GalleryDeleteView.as_view(), name='album-delete'),
    url(r'^albums/(?P<pk>\d+)/', GalleryDetailView.as_view(), name='album-preview'),
    url(r'^pictures/(?P<pk>\d+)/delete/', PictureDeleteView.as_view(), name='picture-delete'),
    url(r'^pictures/(?P<pk>\d+)/', PictureDetailView.as_view(), name='picture-detail'),
    # Wordpress-like media uploader
    url(r'^image/(?P<pk>\d+)/', ImageView.as_view(), name='image'),
    #url(r'^(?P<filename>.*\w+)', UserGalleryView.as_view(), name='gallery_delete'),
    url(r'^update/(?P<pk>\d+)/', UserGalleryUpdateView.as_view(), name='update'),
    url(r'^upload/', UserGalleryCreateView.as_view(), name='upload'),
    url(r'^(?P<username>[\w-]+)/', UserGalleryView.as_view(), name='user_gallery'),
    url(r'^$', UserGalleryView.as_view(), name='index'),
)
