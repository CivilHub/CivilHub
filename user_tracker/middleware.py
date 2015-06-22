# -*- coding: utf-8 -*-
from datetime import timedelta
from ipware.ip import get_ip

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db.utils import DatabaseError
from django.utils import timezone

from .models import Visitor

import logging
log = logging.getLogger('tracking')


NO_TRACKING_PREFIXES = ['/jsi18n/', ]


class VisitorTrackingMiddleware(object):

    def __init__(self):
        """Process the settings before handling the first request."""
        # get a list of URL prefixes that should not be tracked.
        self.prefixes = NO_TRACKING_PREFIXES
        if settings.MEDIA_URL and settings.MEDIA_URL != '/':
            self.prefixes.append(settings.MEDIA_URL)
        if settings.STATIC_URL and settings.STATIC_URL != '/':
            self.prefixes.append(settings.STATIC_URL)

    def process_request(self, request):
        # don't process AJAX requests
        if request.is_ajax():
            return

        ip_address = get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        if hasattr(request, 'session') and request.session.session_key:
            # use the current session key if we can
            session_key = request.session.session_key
        else:
            # otherwise just fake a session key
            session_key = '%s:%s' % (ip_address, user_agent)
            session_key = session_key[:40]

        # ensure that the request.path does not begin with any of the prefixes
        for prefix in self.prefixes:
            if request.path.startswith(prefix):
                return

        # if we get here, the URL needs to be tracked
        now = timezone.now()

        # determine whether or not the user is logged in
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None

        attributes = {
            'user': user,
            'session_key': session_key,
            'ip_address': ip_address
        }

        # see if this is a known visitor, or create a new entry
        try:
            visitor = Visitor.objects.get(**attributes)
        except Visitor.DoesNotExist:
            # see if there's a visitor with the same IP and user agent
            # within the last 5 minutes
            cutoff = now - timedelta(minutes=5)
            visitors = Visitor.objects.filter(
                ip_address=ip_address,
                user_agent=user_agent,
                last_update__gte=cutoff
            )

            if len(visitors):
                visitor = visitors[0]
                visitor.session_key = session_key
            else:
                # it's probably safe to assume that the visitor is brand new
                visitor = Visitor(**attributes)

        # update the tracking information
        visitor.user = user
        visitor.user_agent = user_agent

        # if the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL
        one_hour_ago = now - timedelta(hours=1)
        if not visitor.last_update or visitor.last_update <= one_hour_ago:
            visitor.referrer = request.META.get('HTTP_REFERER',
                                                'unknown')[:255]

            # reset the number of pages they've been to
            visitor.page_views = 0
            visitor.session_start = now

        visitor.url = request.path
        visitor.page_views += 1
        visitor.last_update = now
        try:
            visitor.save()
        except DatabaseError:
            log.error('Problem when saving visitor information')
