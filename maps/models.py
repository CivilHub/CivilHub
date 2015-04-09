# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from locations.models import Location
from .managers import MapPointerManager


class BaseAbstractMapPointer(models.Model):
    """
    An abstract base class that any custom pointer models probably should subclass.
    """
    # Content-object field
    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        abstract = True


@python_2_unicode_compatible
class MapPointer(BaseAbstractMapPointer):
    """ Final MapPointer class. """
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.ForeignKey(Location, null=True, blank=True)

    objects = MapPointerManager()

    def __str__(self):
        return "{},{}".format(self.latitude, self.longitude)


def create_marker(sender, instance, created, **kwargs):
    """ Create map marker for new model instance. """
    if instance.latitude and instance.longitude:
        # Check if created object is location itself:
        if isinstance(instance, Location):
            location = instance
        elif hasattr(instance, 'location'):
            location = instance.location
        mp = MapPointer.objects.create(content_object = instance,
                                       latitude = instance.latitude,
                                       longitude = instance.longitude,
                                       location = location)
        mp.save()


def delete_marker(sender, instance, **kwargs):
    """ Delete all markers related to target model instance. """
    for marker in MapPointer.objects.for_model(instance):
        marker.delete()


# Dirty hack to place it here, but we have circular import with Location model.
models.signals.post_save.connect(create_marker, sender=Location)
models.signals.post_delete.connect(delete_marker, sender=Location)
