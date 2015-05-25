# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class VisitManager(models.Manager):
    """
    Simplify some common function to get counters. This manager is
    made rather to get numeric counter values than querysets.
    """
    def count_for_object(self, instance):
        """ Returns total count for this object. """
        qs = super(VisitManager, self).get_queryset()
        ct = ContentType.objects.get_for_model(instance)
        return sum([x.visit_count for x in qs.filter(
            content_type=ct, object_id=instance.pk)])

    def count_unique_for_object(self, instance):
        """ Count only one visit for each IP address. """
        qs = super(VisitManager, self).get_queryset()
        ct = ContentType.objects.get_for_model(instance)
        return len(qs.filter(content_type=ct, object_id=instance.pk))


class Visit(models.Model):
    """
    This model may be bound with different content. If counter for this content
    already exists, it should just be incremented.
    """
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ip = models.IPAddressField()
    visit_count = models.IntegerField(default=1)

    objects = VisitManager()

    class Meta:
        unique_together = ('ip', 'content_type', 'object_id',)
        verbose_name = _(u"visit counter")
        verbose_name_plural = _(u"visit counters")
