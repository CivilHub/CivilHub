# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.geoip import GeoIP
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


# Default tracking timeout is set to 10 minutes.
TIMEOUT = 10
if hasattr(settings, 'TRACKING_TIMEOUT'):
    TIMEOUT = int(settings.TRACKING_TIMEOUT)


def set_timeout(timeout=None):
    """ Helper for VisitorManager - sets activity time period based on given
        timeout (or default setting, if None is given).
    """
    if timeout is None:
        timeout = TIMEOUT

    now = timezone.now()
    return now - timedelta(minutes=timeout)


class VisitorManager(models.Manager):

    def active(self, timeout=None):
        """
        Retrieves only visitors who have been active within the timeout
        period.
        """
        return self.get_queryset().filter(last_update__gte=set_timeout(timeout))

    def active_users(self, timeout=None):
        """ Retrieve only registered visitors active within timeout period.
        """
        return self.active().filter(user__isnull=False)


    def last_for_user(self, user):
        """ Returns last visitor instance for given user.
        """
        return self.get_queryset().filter(user=user).first()


@python_2_unicode_compatible
class Visitor(models.Model):
    """ This is simplified model taken from django-user-tracking:
        https://bitbucket.org/elevenbits/django-user-tracking/
    """
    session_key = models.CharField(max_length=40, verbose_name=_(u"session key"))
    ip_address = models.CharField(max_length=20, verbose_name=_(u"IP address"))
    user = models.ForeignKey(User, null=True, verbose_name=_(u"user"))
    user_agent = models.CharField(max_length=255, verbose_name=_(u"user agent"))
    referrer = models.CharField(max_length=255, verbose_name=_(u"referrer"))
    url = models.CharField(max_length=255, verbose_name=_(u"url"))
    page_views = models.PositiveIntegerField(default=0, verbose_name=_(u"page views"))
    session_start = models.DateTimeField(verbose_name=_(u"session start"))
    last_update = models.DateTimeField(verbose_name=_(u"last update"))
    checked = models.BooleanField(default=False)

    objects = VisitorManager()

    @property
    def time_on_site(self):
        """
        Attempts to determine the amount of time a visitor has spent on the
        site based upon their information that's in the database.
        """
        if self.session_start:
            seconds = (self.last_update - self.session_start).seconds

            hours = seconds / 3600
            seconds -= hours * 3600
            minutes = seconds / 60
            seconds -= minutes * 60

            return u'%i:%02i:%02i' % (hours, minutes, seconds)
        else:
            return _(u'unknown')

    @property
    def geoip_data(self):
        """
        Attempts to retrieve MaxMind GeoIP data based upon the visitor's IP
        """
        return GeoIP().city(self.ip_address)

    @property
    def geoip_data_json(self):
        """
        Cleans out any dirty unicode characters to make the geoip data safe for
        JSON encoding.
        """
        clean = {}
        if not self.geoip_data:
            return {}

        for key, value in self.geoip_data.items():
            clean[key] = value
        return clean

    def __str__(self):
        return "{}/{} [{} ({})]".format(self.ip_address,
                                        self.session_key,
                                        self.url,
                                        self.page_views)

    class Meta:
        verbose_name = _(u"visitor")
        verbose_name_plural = _(u"visitors")
        ordering = ('-last_update',)
