# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^pointer/', views.CreateMapPoint.as_view(), name='pointer'),
    url(r'^pointers/', views.get_pointers, name='pointers'),
    url(r'^$', views.index, name='index'),
)
