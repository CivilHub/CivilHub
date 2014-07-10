# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from staticpages.views import PageView
admin.autodiscover()
# include action hooks globally
from places_core import actstreams
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
router.register(r'badges', views.BadgeViewSet, base_name=r'badges')
router.register(r'galleries', views.GalleryViewSet, base_name=r'galleries')
router.register(r'idea_votes', views.IdeaVoteCounterViewSet, base_name=r'idea_votes')
router.register(r'usermedia', views.MediaViewSet, base_name=r'usermedia')
router.register(r'my_actions', views.UserActionsRestViewSet, base_name=r'my_actions')
# django sitemaps framework
import places_core.sitemaps as sitemaps
sitemaps = {
    'locations': sitemaps.LocationSitemap,
    'ideas'    : sitemaps.IdeaSitemap,
    'news'     : sitemaps.NewsSitemap,
    'polls'    : sitemaps.PollsSitemap,
    'discussions': sitemaps.DiscussionSitemap,
}
# Javascript translations catalog
js_info_dict = {
    'packages': (
        'comments',
        'blog',
        'gallery',
        'locations',
        'maps',
        'topics',
        'userspace',
    ),
}

urlpatterns = patterns('',
    # user account
    url(r'^user/', include('userspace.urls', namespace='user')),
    url(r'^users/', include('userspace.urls', namespace='user')),
    # Email app
    url(r'^civmail/', include('civmail.urls', namespace='civmail')),
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
    # Static pages
    url(r'^pages/', include('staticpages.urls', namespace='pages')),
    # http://django-generic-bookmarks.readthedocs.org/en/latest
    (r'^bookmarks/', include('bookmarks.urls', namespace='bookmarks')),
    # media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    # REST server
    url(r'^rest/', include(router.urls, namespace='rest')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^search/', include('haystack.urls', namespace='search')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    
    # Static Pages
    # Definicje stron statycznych idą tutaj, metodą kopiego i pejsta można
    # dodawać kolejne.
    url(r'^home/', PageView.as_view(page='home')),
    url(r'^about/', PageView.as_view(page='about')),
    
    # Default URL - Nie wstawiać nic poniżej!!!
    url(r'^$', PageView.as_view(page='home')),
    url(r'^', include('locations.urls', namespace='locations')),
)
