# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from staticpages.views import PageView, HomeView
from userspace.views import UserActivityView
from places_core.views import FileServeView
admin.autodiscover()

from civmail.admin import civmail_admin_site
from places_core import actstreams

# djangorestframework
from rest_framework import routers
from rest import views
router = routers.DefaultRouter()

# Api Views
#router.register(r'news_add', views.SimpleNewsViewSet, base_name="news_add")
router.register(r'current_user', views.CurrentUserViewSet, base_name='current_user')

# Site Views
router.register(r'users', views.UserViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'comments', views.CommentsViewSet, base_name=r'comment')
router.register(r'votes', views.CommentVoteViewSet, base_name=r'vote')
router.register(r'tags', views.TagViewSet, base_name=r'tag')
router.register(r'news', views.NewsViewSet, base_name=r'news')
router.register(r'discussion', views.ForumCategoryViewSet, base_name=r'discussion')
router.register(r'topics', views.ForumViewSet, base_name=r'topics')
router.register(r'replies', views.DiscussionRepliesViewSet, base_name=r'replies')
router.register(r'reports', views.AbuseReportViewSet, base_name=r'reports')
router.register(r'idea_categories', views.IdeaCategoryViewSet, base_name=r'idea_categories')
router.register(r'badges', views.BadgeViewSet, base_name=r'badges')
router.register(r'galleries', views.GalleryViewSet, base_name=r'galleries')
router.register(r'ideas', views.IdeaListViewSet, base_name=r'ideas')
router.register(r'idea_votes', views.IdeaVoteCounterViewSet, base_name=r'idea_votes')
router.register(r'usermedia', views.MediaViewSet, base_name=r'usermedia')
router.register(r'my_actions', views.UserActionsRestViewSet, base_name=r'my_actions')
router.register(r'polls', views.PollListViewSet, base_name=r'polls')
router.register(r'locationlist', views.LocationBasicViewSet, base_name=r'locationlist')
# django sitemaps framework
import places_core.sitemaps as sitemaps
sitemaps = {
    'locations': sitemaps.LocationSitemap,
    'ideas'    : sitemaps.IdeaSitemap,
    'news'     : sitemaps.NewsSitemap,
    'polls'    : sitemaps.PollsSitemap,
    'discussions': sitemaps.DiscussionSitemap,
    'projects': sitemaps.ProjectsSitemap,
    'articles': sitemaps.ArticleSitemap,
    'documents': sitemaps.EtherpadSitemap,
    'organizations': sitemaps.OrganizationSitemap,
    'guides': sitemaps.GuideSitemap,
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

# Django Rest Framework
# ------------------------------------------------------------------------------
from locations.urls import router as location_router
from ideas.urls import router as idea_router
from topics.urls import router as discussion_router
from blog.urls import router as blog_router
from maps.urls import router as map_router
from userspace.urls import router as user_router
from places_core.urls import router as core_router
from gallery.urls import router as gallery_router
from notifications.urls import router as notification_router
from activities.urls import router as activity_router
from hitcounter.urls import router as hitcounter_router
urlpatterns = patterns('',
    url(r'^api-ideas/', include(idea_router.urls)),
    url(r'^api-locations/', include(location_router.urls)),
    url(r'^api-discussions/', include(discussion_router.urls)),
    url(r'^api-blog/', include(blog_router.urls)),
    url(r'^api-maps/', include(map_router.urls)),
    url(r'^api-userspace/', include(user_router.urls)),
    url(r'^api-core/', include(core_router.urls)),
    url(r'^api-gallery/', include(gallery_router.urls)),
    url(r'^api-notifications/', include(notification_router.urls)),
    url(r'^api-activities/', include(activity_router.urls)),
    url(r'^api-hitcounter/', include(hitcounter_router.urls)),
)

from civmail.views import ContactEmailView, InviteFriendsView
urlpatterns += patterns('',
    url(r'^contact/', ContactEmailView.as_view(), name="contact"),
    url(r'^invite-friends/', InviteFriendsView.as_view(), name="invite_friends"),
)

from places_core.views import set_language
urlpatterns += patterns('',
    url(r'^', include('hitcounter.urls')),
    url(r'^guides/', include('guides.urls', namespace="guides")),
    url(r'^organizations/', include('organizations.urls', namespace="organizations")),
    url(r'^simpleblog/', include('simpleblog.urls', namespace="simpleblog")),
    # user account
    url(r'^user/', include('userspace.urls', namespace='user')),
    url(r'^users/', include('userspace.urls', namespace='user')),
    url(r'^bookmarks/', include('bookmarks.urls')),
    # Email app
    url(r'^civmail/', include('civmail.urls', namespace='civmail')),
    url(r'^civmail-admin/', include(civmail_admin_site.urls)),
    # Maps
    url(r'^maps/', include('maps.urls', namespace='maps')),
    # blog
    url(r'^news/', include('blog.urls', namespace='blog')),
    # ideas
    url(r'^ideas/', include('ideas.urls', namespace='ideas')),
    # django-activity-stream
    url(r'^activity/', UserActivityView.as_view()),
    # social auth
    url('', include('social.apps.django_app.urls', namespace='social')),
    # django-discussions (e.g. user messages)
    # disabled because of lack South integrity
    #url('^messages/', include('discussions.urls', namespace='messages')),
    # Basic project views - the rest is within locations
    url('^projects/', include('projects.urls', namespace='projects')),
    # Discussions (e.g. forum)
    url('^discussion/', include('topics.urls', namespace='discussion')),
    # comments
    url('^comments/', include('comments.urls', namespace='comments')),
    # admin panel
    url(r'^fuck-off-i-am-awesome/', include(admin.site.urls)),
    # Abuse reports (static)
    url(r'^report/', include('places_core.urls', namespace='reports')),
    # User media
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    # Polls app
    url(r'^polls/', include('polls.urls', namespace='polls')),
    # Static pages
    url(r'^pages/', include('staticpages.urls', namespace='pages')),
    # media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    # REST server
    url(r'^rest/', include(router.urls, namespace='rest')),
    # Haystack - search engine
    url(r'^search/', include('haystack.urls', namespace='search')),
    # django-messages: messages between users
    url(r'^messages/', include('postman.urls')),
    # Language support
    url(r'^i18n/setlang', set_language, name='set_language'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    # For robots - indexers :)
    url(r'^robots.txt$', FileServeView.as_view(filename='robots.txt')),
    # Captcha
    url(r'^captcha/', include('captcha.urls')),
    # Static Pages
    # Definition of static pages go here, you can add new ones by
    # copy-paste method.
    url(r'^home/', PageView.as_view(page='home')),
    url(r'^home-b/', PageView.as_view(page='home-b')),
    url(r'^home-c/', PageView.as_view(page='home-c')),
    url(r'^home-d/', PageView.as_view(page='home-d')),
    url(r'^home-e/', PageView.as_view(page='home-e')),
    url(r'^home-f/', PageView.as_view(page='home-f')),
    url(r'^home-g/', PageView.as_view(page='home-g')),
    url(r'^home-h/', PageView.as_view(page='home-h')),
    url(r'^home-i/', PageView.as_view(page='home-i')),
    url(r'^home-j/', PageView.as_view(page='home-j')),

    #url(r'^about/', PageView.as_view(page='about')),
    #url(r'^privacy/', PageView.as_view(page='privacy')),
    #url(r'^terms/', PageView.as_view(page='terms')),
    #url(r'^cookies/', PageView.as_view(page='cookies')),
    #url(r'^contact/', PageView.as_view(page='contact')),
    #url(r'^jobs/', PageView.as_view(page='jobs')),
    #url(r'^press/', PageView.as_view(page='press')),
    #url(r'^mission/', PageView.as_view(page='mission')),
    #url(r'^team/', PageView.as_view(page='team')),
    #url(r'^values/', PageView.as_view(page='values')),
    #url(r'^creed/', PageView.as_view(page='creed')),
    #url(r'^support/', PageView.as_view(page='support')),
    url(r'^feature/', PageView.as_view(page='feature')),

    # Etherpad - live collaboration tool
    url(r'^', include('etherpad.urls')),

    # Notifications for users - mainly views for testing.
    url(r'^', include('notifications.urls')),

    # Default URL - Do not add anything below!!!
    #url(r'^$', PageView.as_view(page='home')),
    url(r'^$', HomeView.as_view()),

    #url(r'^$', staticpages.views.HomeView.as_view()),
    url(r'^', include('articles.urls', namespace='articles')),
    url(r'^', include('locations.urls', namespace='locations')),
)

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)
