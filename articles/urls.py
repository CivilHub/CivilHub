# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^contact/', views.TopLevelArticleView.as_view(article_slug='contact'), name='contact'),
    url(r'^cookies/', views.TopLevelArticleView.as_view(article_slug='cookies'), name='cookies'),
    url(r'^privacy/', views.TopLevelArticleView.as_view(article_slug='privacy'), name='privacy'),
    url(r'^about-us/', views.TopLevelArticleView.as_view(article_slug='about-us'), name='about-us'),
    url(r'^creed/', views.TopLevelArticleView.as_view(article_slug='creed'), name='creed'),
    url(r'^press/', views.TopLevelArticleView.as_view(article_slug='press'), name='press'),
    url(r'^terms/', views.TopLevelArticleView.as_view(article_slug='terms'), name='terms'),
    url(r'^jobs/', views.TopLevelArticleView.as_view(article_slug='jobs'), name='jobs'),
    url(r'^features/', views.TopLevelArticleView.as_view(article_slug='features', template_name='articles/features.html'), name='features'),
    url(r'^team/', views.TopLevelArticleView.as_view(article_slug='team', template_name='articles/clear.html'), name='team'),
    url(r'^blog/(?P<slug>[\w-]+)/', views.BlogEntryView.as_view(), name='blog_entry'),
    url(r'^blog/', views.BlogListView.as_view(), name='blog'),
    #url(r'^support/(?P<slug>[\w-]+)/', views.SupportEntryView.as_view(), name='support_entry'),
    #url(r'^support/', views.SupportListView.as_view(), name='support'),
    url(r'^support/', views.TopLevelArticleView.as_view(article_slug='support', template_name='articles/support-list.html'), name='support'),
    url(r'^vector-map/', views.TopLevelArticleView.as_view(article_slug='vector-map', template_name='articles/vector-map.html'), name='vector-map'),
    url(r'^do-testowania/', views.TopLevelArticleView.as_view(article_slug='do-testowania', template_name='articles/test.html'), name='do-testowania'),
    url(r'^brief/', views.TopLevelArticleView.as_view(article_slug='brief', template_name='articles/brief.html'), name='brief')
)
