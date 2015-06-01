# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

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
    location = models.ForeignKey('locations.Location', null=True, blank=True)

    objects = MapPointerManager()

    def __str__(self):
        return "{},{}".format(self.latitude, self.longitude)

    class Meta:
        unique_together = ('latitude', 'longitude',
                           'object_pk', 'content_type', )
