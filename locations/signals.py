# -*- coding: utf-8 -*-
from django.core import cache
from django.conf import settings

redis_cache = cache.get_cache('default')


def update_parent_cache(sender, instance, created, **kwargs):
    """ Update cached lists of sublocations for parent location. """
    if not created or instance.parent is None:
        return True
    for language in [x[0] for x in settings.LANGUAGES]:
        key = "{}_{}_sub".format(instance.parent.slug, language)
        redis_cache.set(key, instance.parent.location_set.all())


def adjust_created_location(sender, instance, created, **kwargs):
    """ Location creator will be moderator and follower. """
    if created:
        instance.creator.profile.mod_areas.add(instance)
        instance.creator.profile.save()
