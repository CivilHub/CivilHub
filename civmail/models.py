# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone, translation
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from messages import MassMailTemplate


@python_2_unicode_compatible
class MassEmail(models.Model):
    """ Translatable message to everyone.
    """
    STATUS_CHOICES = (
        (1, _(u"pending")),
        (2, _(u"sent")),
    )
    subject = models.CharField(max_length=64, default="", verbose_name=_(u"subject"))
    body = models.TextField(default="", verbose_name=_(u"message"))
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1, verbose_name=_(u"status"))
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name=_(u"date sent"))
    scheduled_at = models.DateTimeField(blank=True, null=True, verbose_name=_(u"scheduled at"))

    def send(self):
        message_context = {'message': self, }
        for recipient in User.objects.all():
            translation.activate(recipient.profile.lang)
            message_context.update({'lang': recipient.profile.lang, })
            MassMailTemplate().send(recipient.email, message_context)
            translation.deactivate()
        self.status = 2
        self.sent_at = timezone.now()
        self.save()

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _(u"mass email")
        verbose_name_plural = _(u"mass emails")
