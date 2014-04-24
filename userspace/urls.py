# -*- coding: utf-8 -*-
from django.conf.urls import url
from userspace import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'register/', views.register, name='register'),
    url(r'passet/', views.passet, name='passet'),
    url(r'chpass/', views.chpass, name='chpass'),
    url(r'upload_avatar/', views.upload_avatar, name='upload_avatar'),
    url(r'save_settings/', views.save_settings, name='save_settings'),
]