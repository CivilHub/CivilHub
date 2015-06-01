# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text


class MapPointerManager(models.Manager):
    """ A manager for map markers - filtered through the location or object.
    """
    def for_model(self, model):
        """ QuerySet for all pointers for a particular model.
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs

    def for_location(self, location):
        """ QuerySet for all pointers for particular location.
        """
        return self.get_queryset().filter(location=location)

    def create_for_object(self, obj, lat, lng, **kwargs):
        """ Creates new map pointer for given object on passed latitude and longitude.
        """
        pointer = self.model(latitude=lat, longitude=lng, object_pk=obj.pk,
                             content_type=ContentType.objects.get_for_model(obj))
        if obj._meta.model_name == 'location':
            pointer.location = obj
        elif hasattr(obj, 'location'):
            pointer.location = obj.location
        pointer.save()
        return pointer
