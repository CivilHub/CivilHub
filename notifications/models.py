# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import striptags, truncatechars
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class NotificationManager(models.Manager):
    """
    Allows faster counting and searching for notifications related to user.
    """

    def count_unread_for_user(self, user):
        """ This method takes user instance and returns number of unread
        notifications belonging to him. """
        qs = super(NotificationManager, self).get_queryset()
        return qs.filter(user=user, checked_at__isnull=True).count()

    def unread_for_user(self, user):
        """ Find all unread notifications for particular user instance. """
        qs = super(NotificationManager, self).get_queryset()
        return qs.filter(user=user, checked_at__isnull=True)


@python_2_unicode_compatible
class Notification(models.Model):
    """
    Basic model for all notifications.
    """
    user = models.ForeignKey(User,
                             related_name="notifications",
                             verbose_name=_(u"user"))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u"date created"))
    checked_at = models.DateTimeField(blank=True,
                                      null=True,
                                      verbose_name=_(u"read at"))
    # We can pass arbitrary keyword to simplify notification management
    key = models.CharField(max_length=32,
                           blank=True,
                           default="",
                           verbose_name=_(u"keyword"))
    # This will be part of human-friendly description
    action_verb = models.CharField(max_length=64,
                                   blank=True,
                                   null=True,
                                   verbose_name=_(u"verb"))
    action_actor = models.ForeignKey(User,
                                     related_name="made_notifications",
                                     blank=True,
                                     null=True,
                                     verbose_name=_(u"actor"))
    # This will work like similar fields in activity stream
    # We take some object involved in action...
    action_object_ct = models.ForeignKey(ContentType,
                                         blank=True,
                                         null=True,
                                         related_name="notify_action_objects")
    action_object_id = models.PositiveIntegerField(blank=True, null=True)
    action_object = generic.GenericForeignKey('action_object_ct',
                                              'action_object_id')
    # ...and it's target
    action_target_ct = models.ForeignKey(ContentType,
                                         blank=True,
                                         null=True,
                                         related_name="notify_action_targets")
    action_target_id = models.PositiveIntegerField(blank=True, null=True)
    action_target = generic.GenericForeignKey('action_target_ct',
                                              'action_target_id')

    objects = NotificationManager()

    @property
    def is_new(self):
        return self.checked_at is None

    def read(self):
        if not self.checked_at:
            self.checked_at = timezone.now()
            self.save()

    def get_absolute_url(self):
        return reverse('notify-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.action_verb is not None:
            self.action_verb = truncatechars(striptags(self.action_verb), 64)
        super(Notification, self).save(*args, **kwargs)

    def __str__(self):
        return u"Notification #{} for user {}".format(self.pk, self.user.email)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = _(u"notification")
        verbose_name_plural = _(u"notifications")


def notify(actor, user, **kwargs):
    """ Create proper notification based on passed values. """
    notify = Notification(user=user, action_actor=actor)
    action_object = kwargs.get('action_object')
    if action_object is not None:
        notify.action_object_ct = ContentType.objects.get_for_model(action_object)
        notify.action_object_id = action_object.pk
    action_target = kwargs.get('action_target')
    if action_target is not None:
        notify.action_target_ct = ContentType.objects.get_for_model(action_target)
        notify.action_target_id = action_target.pk
    keyword = kwargs.get('key')
    if keyword is not None:
        notify.key = keyword
    verb = kwargs.get('verb')
    if verb is not None:
        notify.action_verb = verb
    notify.save()
