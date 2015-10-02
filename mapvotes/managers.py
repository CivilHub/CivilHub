# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType


class VotingManager(models.Manager):
    """ Custom manager for ``Voting``, which provides shortcut method for
    creating and retrieving votings related to specific model instances.

    TODO: Implement ``get_or_create_for_instance`` method.
    """
    def get_for_instance(self, instance=None):
        if instance is None:
            return self.get_queryset().none()
        ct = ContentType.objects.get_for_model(instance)
        return self.get_queryset().filter(content_type=ct,
                                          object_id=instance.pk)

    def create_for_instance(self, instance=None, **kwargs):
        ct = ContentType.objects.get_for_model(instance)
        obj = self.model(**kwargs)
        obj.content_type = ct
        obj.object_id = instance.pk
        obj.save()
        return obj

