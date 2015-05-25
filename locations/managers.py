# -*- coding: utf-8 -*-
from django.db import models
from django.utils import translation

from places_core.helpers import sort_by_locale


class LocationLocaleManager(models.Manager):
    """
    A manager that allows to order locations albhabetically with local utf-8 signs
    taken into account.
    """
    def get_queryset(self):
        return sort_by_locale(super(LocationLocaleManager, self).get_queryset(),
                        lambda x: x.__unicode__(), translation.get_language())
