# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from locations.models import Location
from organizations.models import Organization
from places_core.permissions import is_moderator
from projects.models import SlugifiedModelMixin


@python_2_unicode_compatible
class GuideCategory(models.Model):
    """ Very simple model for category.
    """
    name = models.CharField(max_length=64, verbose_name=_(u"name"))
    description = models.TextField(blank=True, default="", verbose_name=_(u"description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"category")
        verbose_name_plural = _(u"categories")


@python_2_unicode_compatible
class GuideTag(models.Model):
    """ Tags may be related to many published guides.
    """
    name = models.CharField(max_length=64, verbose_name=_(u"name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"tag")
        verbose_name_plural = _(u"tags")


@python_2_unicode_compatible
class Guide(SlugifiedModelMixin):
    """
    Core model for this application - the guide itself. This model holds a lot
    of foreign relations. It may be published in one or more locations and we
    can also add NGO to participate. There may be also more than one author.
    """
    STATUS_CHOICES = (
        (1, _(u"draft")),
        (2, _(u"published")),
    )
    owner = models.ForeignKey(User, related_name="owned_guides", verbose_name=_(u"owner"))
    editors = models.ManyToManyField(User, related_name="permitted_guides", verbose_name=_(u"editors"), blank=True, null=True,
        help_text=_(u"Select people permitted to modify this guide. You don't have to include yourself if you're owner."))
    content = models.TextField(default="", verbose_name=_(u"content"))
    authors = models.ManyToManyField(User, blank=True, null=True, verbose_name=_(u"authors"), related_name="authored_guides")
    location = models.ForeignKey(Location, verbose_name=_(u"location"), related_name="guides")
    tags = models.ManyToManyField(GuideTag, blank=True, null=True, verbose_name=_(u"tags"))
    category = models.ForeignKey(GuideCategory, blank=True, null=True, verbose_name=_(u"category"), related_name="guides")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_(u"last modified"))
    organizations = models.ManyToManyField(Organization, blank=True, null=True, verbose_name=_(u"organizations"), related_name="guides")
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1, verbose_name=_(u"status"))

    def get_absolute_url(self):
        return reverse('guides:detail', kwargs={
            'location_slug': self.location.slug,
            'slug': self.slug, })

    def has_access(self, user):
        access = False
        if user.is_superuser:
            access = True
        elif user == self.owner:
            access = True
        elif user in self.editors.all():
            access = True
        elif is_moderator(user, self.location):
            access = True
        return access

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"guide")
        verbose_name_plural = _(u"guides")
