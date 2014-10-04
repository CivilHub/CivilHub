# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

# REST API
from rest.routers import HybridRouter
router = HybridRouter()
router.register('pointers', views.MapPointerAPIViewSet, 'pointers')
router.register('objects', views.MapObjectAPIViewSet, 'objects')
router.add_api_view('data', url(r'^data/$', views.MapDataViewSet.as_view(), name='data'))


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
)
