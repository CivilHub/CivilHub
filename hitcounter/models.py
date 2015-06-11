# -*- coding: utf-8 -*-
import collections
import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
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

    def graph_data(self, obj):
        qs = super(VisitManager, self).get_queryset()
        ct = ContentType.objects.get_for_model(obj)
        all_visits = qs.filter(
            content_type=ct, object_id=obj.pk).order_by('date')

        start_time = all_visits.first().date
        stop_time = timezone.now()

        results = []
        the_time = start_time
        while the_time < stop_time + datetime.timedelta(hours=12):
            results.append(all_visits.filter(date__year=the_time.year,
                                             date__month=the_time.month,
                                             date__day=the_time.day).count())
            the_time = the_time + datetime.timedelta(days=1)

        Serializer = collections.namedtuple('Serializer',
                        ['counter', 'title', 'start', 'results'])
        return Serializer(counter=all_visits.count(),
                          title=obj.__unicode__(),
                          start=str(start_time),
                          results=results)


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
        verbose_name = _(u"visit counter")
        verbose_name_plural = _(u"visit counters")
