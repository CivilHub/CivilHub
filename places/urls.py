# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
# djangorestframework
from rest_framework import routers
from rest import views
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'comments', views.CommentsViewSet, base_name=r'comment')
router.register(r'votes', views.CommentVoteViewSet, base_name=r'vote')
router.register(r'tags', views.TagViewSet, base_name=r'tag')
router.register(r'news', views.NewsViewSet, base_name=r'news')
router.register(r'discussion', views.ForumCategoryViewSet, base_name=r'discussion')
router.register(r'reports', views.AbuseReportViewSet, base_name=r'reports')
router.register(r'ideas', views.IdeaCategoryViewSet, base_name=r'ideas')
# django sitemaps framework
import places_core.sitemaps as sitemaps
sitemaps = {
    'locations': sitemaps.LocationSitemap,
    'ideas'    : sitemaps.IdeaSitemap,
    'news'     : sitemaps.NewsSitemap,
    'polls'    : sitemaps.PollsSitemap,
    'discussions': sitemaps.DiscussionSitemap,
}

urlpatterns = patterns('',
    # user account
    url(r'^user/', include('userspace.urls', namespace='user')),
    url(r'^users/', include('userspace.urls', namespace='user')),
    # Google Maps
    url(r'^maps/', include('maps.urls', namespace='maps')),
    # blog
    url(r'^blog/', include('blog.urls', namespace='blog')),
    # ideas
    url(r'^ideas/', include('ideas.urls', namespace='ideas')),
    # django-activity-stream
    url(r'^activity/', include('actstream.urls', namespace='activities')),
    # social auth
    url('', include('social.apps.django_app.urls', namespace='social')),
    # django-discussions (e.g. user messages)
    # disabled because of lack South integrity
    #url('^messages/', include('discussions.urls', namespace='messages')),
    # Discussions (e.g. forum)
    url('^discussion/', include('topics.urls', namespace='discussion')),
    # comments
    url('^comments/', include('comments.urls', namespace='comments')),
    # admin panel
    url(r'^admin/', include(admin.site.urls)),
    # Abuse reports (static)
    url(r'^report/', include('places_core.urls', namespace='reports')),
    # User media
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    # Polls app
    url(r'^polls/', include('polls.urls', namespace='polls')),
    # http://django-generic-bookmarks.readthedocs.org/en/latest
    (r'^bookmarks/', include('bookmarks.urls', namespace='bookmarks')),
    # media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    # REST server
    url(r'^rest/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^search/', include('haystack.urls', namespace='search')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^', include('locations.urls', namespace='locations')),
)
