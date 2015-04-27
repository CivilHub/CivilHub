# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^accept/(?P<key>[\w-]+)/', views.InviteAcceptView.as_view(), name="accept"),
    url(r'^create/', views.OrganizationCreateView.as_view(), name="create"),
    url(r'^(?P<slug>[\w-]+)/background/', views.NGOBackgroundView.as_view(), name="background"),
    url(r'^(?P<slug>[\w-]+)/news/create/', views.NGONewsCreate.as_view(), name="news-create"),
    url(r'^(?P<slug>[\w-]+)/news/(?P<news_slug>[\w-]+)/', views.NGONewsDetail.as_view(), name="news-detail"),
    url(r'^(?P<slug>[\w-]+)/news/', views.NGONewsList.as_view(), name="news-list"),
    url(r'^(?P<slug>[\w-]+)/projects/add/', views.NGOProjectAdd.as_view(), name="project-add"),
    url(r'^(?P<slug>[\w-]+)/projects/', views.NGOProjectList.as_view(), name="project-list"),
    url(r'^(?P<slug>[\w-]+)/invite/', views.InviteUsers.as_view(), name="invite"),
    url(r'^(?P<slug>[\w-]+)/update/', views.OrganizationUpdateView.as_view(), name="update"),
    url(r'^(?P<slug>[\w-]+)/members/', views.OrganizationMemberList.as_view(), name="members"),
    url(r'^(?P<slug>[\w-]+)/member-delete/', views.OrganizationMemberDelete.as_view(), name="member-delete"),
    url(r'^(?P<slug>[\w-]+)/locations/', views.OrganizationLocationList.as_view(), name="locations"),
    url(r'^(?P<slug>[\w-]+)/location-add/', views.OrganizationLocationAdd.as_view(), name="location-add"),
    url(r'^(?P<slug>[\w-]+)/location-delete/', views.OrganizationLocationDelete.as_view(), name="location-delete"),
    url(r'^(?P<slug>[\w-]+)/about/', views.OrganizationView.as_view(template_name='organizations/organization_info.html'), name="info"),
    url(r'^(?P<slug>[\w-]+)/', views.OrganizationView.as_view(), name="detail"),
    url(r'^', views.OrganizationListView.as_view(), name="index"),
)
