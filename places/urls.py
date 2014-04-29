# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # user account
    url(r'^user/', include('userspace.urls', namespace='user')),
    url(r'^users/', include('userspace.urls', namespace='user')),
    # places
    url(r'^places/', include('locations.urls', namespace='locations')),
    # blog
    url(r'^blog/', include('blog.urls', namespace='blog')),
    # ideas
    url(r'^ideas/', include('ideas.urls', namespace='ideas')),
    # django-activity-stream
    url(r'^activity/', include('actstream.urls', namespace='activities')),
    # social auth
    url('', include('social.apps.django_app.urls', namespace='social')),
    # admin panel
    url(r'^admin/', include(admin.site.urls)),
    # media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

# comments
urlpatterns += patterns('',
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
