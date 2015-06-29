# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


class BlessManager(models.Manager):
    """ Simplify generic foreign relations to avoid common ContentType imports.
    """
    def for_model(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        qs = super(BlessManager, self).get_queryset()
        return qs.filter(content_type=ct, object_pk=obj.pk)

    def for_user(self, user):
        return super(BlessManager, self).get_queryset().filter(user=User)


@python_2_unicode_compatible
class Blessing(models.Model):
    """ Schema for recommendation model. We call it 'the bless'.
    """
    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_pk')
    user = models.ForeignKey(User, related_name='recommendations')
    date = models.DateTimeField(auto_now_add=True)

    objects = BlessManager()

    def __str__(self):
        return _(u"Recommendation from") + ' ' + self.user.get_full_name()

    class Meta:
        ordering = ('-date', )
        unique_together = ('user', 'content_type', 'object_pk', )
        verbose_name = _(u"recommendation")
        verbose_name_plural = _(u"recommendations")


# Shortcuts

def bless(user, obj):
    ct = ContentType.objects.get_for_model(obj)
    bless, is_new = Blessing.objects.get_or_create(user=user,
                                                   content_type=ct,
                                                   object_pk=obj.pk)
    if not is_new:
        bless.delete()
    count = Blessing.objects.for_model(obj).count()
    context = {'count': count, 'last': None, 'bless': is_new, }
    if not count:
        return context
    if is_new:
        last_bless = bless
    else:
        last_bless = Blessing.objects.for_model(obj).first()
    context.update({'last': last_bless, })
    return context


def curse(user, obj):
    try:
        bless = Bless.objects.get.filter(content_object=obj, user=user)
        bless.delete()
    except Bless.DoesNotExist:
        pass
