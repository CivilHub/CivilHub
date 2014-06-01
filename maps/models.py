# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from .managers import MapPointerManager


class BaseAbstractMapPointer(models.Model):
    """
    An abstract base class that any custom pointer models probably should
    subclass.
    """

    # Content-object field
    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    class Meta:
        abstract = True


class MapPointer(BaseAbstractMapPointer):
    """
    Final MapPointer class.
    """
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Manager
    objects = MapPointerManager()

    def __unicode__(self):
        return "x".join([str(self.latitude), str(self.longitude)])
