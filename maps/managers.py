# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from locations.models import Location


class MapPointerManager(models.Manager):

    def for_model(self, model):
        """
        QuerySet for all pointers for a particular model.
        """
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=ct)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_text(model._get_pk_val()))
        return qs

    def for_location(self, location):
        """
        QuerySet for all pointers for particular location.
        """
        ids = []
        qs = self.get_queryset()
        for m in qs:
            if m.content_object == location:
                ids.append(m.pk)
            elif hasattr(m.content_object, 'location') and m.content_object.location == location:
                ids.append(m.pk)
        return qs.filter(pk__in=ids)
