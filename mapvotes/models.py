# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import VotingManager


@python_2_unicode_compatible
class Voting(models.Model):
    """ This is voting base. This model is foreign key for all markers created
    within this particular voting. Every marker with FK to instance of this
    model will be taken into account when calculating vote results.

    Voting may be optionally bind to some other model throught generic relation.
    Additionaly we provide custom manager that simplifies creating and
    retrieving votings related to other model instances.
    """
    author = models.ForeignKey('auth.User', verbose_name=_("author"))
    label = models.CharField(_("label"), max_length=64)
    description = models.TextField(_("description"), default="", blank=True)
    start_date = models.DateTimeField(_("start"), null=True, blank=True)
    finish_date = models.DateTimeField(_("finish"), null=True, blank=True)
    is_public = models.BooleanField(_("public"), default=False,
        help_text=_("Allow other users to manage markers"))
    is_limited = models.BooleanField(_("limited"), default=False,
        help_text=_("Limit user votes to just one marker in set"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    # Generic relation is optional
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = VotingManager()

    class Meta:
        verbose_name = _("voting")
        verbose_name_plural = _("votings")

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        if self.content_object is not None:
            # Additional special cases (e.g. specific models) may go here
            if self.content_object._meta.model_name == 'socialproject':
                return reverse('projects:voting', kwargs={
                    'project_slug': self.content_object.slug, 'pk': self.pk})
            return self.content_object.get_absolute_url()
        return "/"

    def is_active(self):
        NOW = timezone.now()
        if self.start_date is not None and NOW < self.start_date:
            return False
        if self.finish_date is not None and NOW > self.finish_date:
            return False
        return True


@python_2_unicode_compatible
class Marker(models.Model):
    """ Represents single object for which users can vote. Voting is limited
    only for authenticated users.
    """
    voting = models.ForeignKey(Voting, verbose_name=_("voting"),
                               related_name="markers")
    lat = models.DecimalField(_("latitude"), max_digits=9, decimal_places=6)
    lng = models.DecimalField(_("longitude"), max_digits=9, decimal_places=6)
    label = models.CharField(_("label"), max_length=64, default="")
    description = models.TextField(_("description"), max_length=2000,
                                   blank=True, default="")

    class Meta:
        verbose_name = _("marker")
        verbose_name_plural = _("markers")

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return self.voting.get_absolute_url()

    def vote(self, user):
        """ Wrapper for votes models. Use this instead of creating ``Vote``
        instances from scratch, as this takes ``Voting`` settings into
        account. """
        try:
            vote = self.votes.get(user=user)
            vote.delete()
            return {'success': True, 'status': False}
        except Vote.DoesNotExist:
            vote = None
        if self.voting.is_limited:
            markers = self.voting.markers.exclude(pk=self.pk)
            chk = sum([x.votes.filter(user=user).count() for x in markers])
            if chk:
                return {'success': False, 'error': _("Too many votes")}
        vote = Vote.objects.create(marker=self, user=user)
        return {'success': True, 'status': True}


@python_2_unicode_compatible
class Vote(models.Model):
    """ The essential part of application.
    """
    user = models.ForeignKey('auth.User', verbose_name=_("user"))
    marker = models.ForeignKey(Marker, verbose_name=_("marker"),
                               related_name="votes")
    date = models.DateTimeField(_("date"), auto_now_add=True)

    class Meta:
        verbose_name = _("vote")
        verbose_name_plural = _("votes")
        unique_together = ('user', 'marker',)

    def __str__(self):
        return _("Vote: {}").format(self.user.get_full_name)

