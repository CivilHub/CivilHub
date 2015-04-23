  # -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from locations.models import BackgroundModelMixin, Location
from projects.models import SlugifiedModelMixin, SocialProject
from userspace.helpers import random_string


def logo_upload_path(instance, filename):
    """
    Provides unique name for logo image.
    """
    return 'img/ngo/' + uuid4().hex + os.path.splitext(filename)[1]


def background_upload_path(instance, filename):
    """
    Provides unique name for background image.
    """
    return 'img/organizations/' + uuid4().hex + os.path.splitext(filename)[1]


@python_2_unicode_compatible
class Category(models.Model):
    """
    Every NGO may fall into one category.
    """
    name = models.CharField(max_length=64, verbose_name=_(u"name"))
    description = models.TextField(blank=True,
                                   default="",
                                   verbose_name=_(u"description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"category")
        verbose_name_plural = _(u"categories")


@python_2_unicode_compatible
class Organization(SlugifiedModelMixin, BackgroundModelMixin):
    """
    Schema and methods for NGO.
    """
    category = models.ForeignKey(Category,
                                 blank=True,
                                 null=True,
                                 verbose_name=_(u"category"))
    description = models.TextField(blank=True,
                                   default="",
                                   verbose_name=_(u"description"))
    creator = models.ForeignKey(User,
                                related_name=_("created_organizations"),
                                verbose_name=_(u"creator"))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_(u"date created"))
    date_modified = models.DateTimeField(auto_now=True,
                                         verbose_name=_(u"date modified"))
    krs = models.CharField(max_length=255,
                           blank=True,
                           default="",
                           verbose_name=_(u"KRS"))
    email = models.EmailField(null=True,
                              blank=True,
                              verbose_name=_(u"contact mail"))
    website = models.URLField(blank=True,
                              null=True,
                              verbose_name=_(u"website"))
    users = models.ManyToManyField(User,
                                   related_name="organizations",
                                   verbose_name=_(u"members"),
                                   blank=True,
                                   null=True)
    locations = models.ManyToManyField(Location,
                                       related_name="organizations",
                                       verbose_name=_(u"locations"),
                                       blank=True,
                                       null=True)
    projects = models.ManyToManyField(SocialProject,
                                      related_name="mentors",
                                      blank=True,
                                      null=True)
    logo = models.ImageField(upload_to=logo_upload_path,
                             default='img/ngo/default.jpg')
    verified = models.BooleanField(default=False,
                                   verbose_name=_(u"is verified"))
    image = models.ImageField(upload_to=background_upload_path,
                              default='img/organizations/default.jpg',
                              verbose_name=_(u"background image"))
    tags = models.CharField(max_length=255,
                            verbose_name=_(u"tags"),
                            blank=True,
                            default="",
                            help_text=_("Tags separated by comma"))

    def get_absolute_url(self):
        return reverse('organizations:detail', kwargs={'slug': self.slug, })

    def has_access(self, user):
        """
        Simple permission check - only superadmin and creator can change object.
        """
        if user.is_superuser:
            return True
        return user == self.creator

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"organization")
        verbose_name_plural = _(u"organizations")


@python_2_unicode_compatible
class Invitation(models.Model):
    """
    Organization's creator and superusers may invite others to join. Invited
    user have to confirm that he actually want to to that.
    """
    user = models.ForeignKey(User, related_name="ngo_invitations")
    organization = models.ForeignKey(Organization,
                                     related_name="invitations",
                                     verbose_name=_(u"organization"))
    key = models.CharField(max_length=255,
                           blank=True,
                           verbose_name=_(u"key"),
                           unique=True)
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_(u"date created"))
    date_accepted = models.DateTimeField(blank=True,
                                         null=True,
                                         verbose_name=_(u"date accepted"))
    is_accepted = models.BooleanField(default=False,
                                      verbose_name=_(u"is accepted"))

    def accept(self):
        self.date_accepted = timezone.now()
        self.is_accepted = True
        self.save()
        if self.user not in self.organization.users.all():
            self.organization.users.add(self.user)
            self.organization.save()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = random_string(255)
        super(Invitation, self).save(*args, **kwargs)

    def __str__(self):
        return u"Invitation to {}".format(self.organization)

    class Meta:
        unique_together = ('user', 'organization', )
        verbose_name = _(u"invitation")
        verbose_name_plural = _(u"invitations")
