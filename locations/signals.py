# -*- coding: utf-8 -*-
from django.core import cache
from django.conf import settings
from django.db.models import signals

redis_cache = cache.get_cache('default')

def update_parent_cache(sender, instance, created, **kwargs):
    """ Update cached lists of sublocations for parent location. """
    if not created or not hasattr(instance, 'parent'):
        return True
    slug = instance.parent.slug
    for language in [x[0] for x in settings.LANGUAGES]:
        key = "{}_{}_sub".format(instance.parent.slug, language)
        redis_cache.set(key, instance.parent.location_set.all())
