# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ContentGalleryManager(models.Manager):
    """ """

    def for_object(self, obj):
        ct = ContentType.objects.get_for_model(obj).pk
        return super(ContentGalleryManager, self).get_queryset()\
            .filter(content_type__id=ct, object_id=obj.pk)
