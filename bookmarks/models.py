# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Bookmark(models.Model):
    """ Universal bookmark for different content types. """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, blank=True, null=True, 
        related_name='bookmarks')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'user')

    def url(self):
        """ Returns objects absolute url if it exists. """
        if hasattr(self.content_object, 'get_absolute_url'):
            return self.content_object.get_absolute_url()
        return None

    def __str__(self):
        """ Try to return objects name. """
        if not hasattr(self.content_object, '__unicode__'):
            return u"Bookmark"
        return self.content_object.__unicode__()
