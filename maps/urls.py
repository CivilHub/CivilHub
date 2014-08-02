# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

# REST API
from rest_framework import routers
router = routers.DefaultRouter()
router.register('pointers', views.MapPointerAPIViewSet, 'pointers')
router.register('objects', views.MapObjectAPIViewSet, 'objects')
router.register('data', views.MapDataViewSet, 'data')


urlpatterns = patterns('',
    url(r'^save/', views.save_pointer, name='save'),
    url(r'^pointer/', views.CreateMapPoint.as_view(), name='pointer'),
    url(r'^pointers/', views.get_pointers, name='pointers'),
    url(r'^remove/', views.delete_pointer, name='remove'),
    url(r'^$', views.index, name='index'),
)
