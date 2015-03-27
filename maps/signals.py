# -*- coding: utf-8 -*-
from django.core import cache
from django.conf import settings
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType

from locations.models import Location

from .models import MapPointer
from .helpers import create_country_clusters


redis_cache = cache.get_cache('default')


def update_marker_cache(sender, instance, **kwargs):
    """
    Update cached pointer objects for map every time new map pointer is created.
    This way we can use redis-server as database with quick access.
    """
    if not instance.location:
        return False
    if instance.location.parent is not None:
        count = MapPointer.objects.filter(
            location__in=instance.location.parent.get_children_id_list()).count()
        redis_cache.set(str(instance.location.pk) + '_childlist', count, timeout=None)
    redis_cache.set('allcountries', create_country_clusters(), timeout=None)


def create_marker(sender, instance, created, **kwargs):
    """ Create map marker for new model instance. """
    if created and instance.latitude and instance.longitude:
        # Check if created object is location itself:
        if isinstance(instance, Location):
            location = instance
        elif hasattr(instance, 'location'):
            location = instance.location

        mp = MapPointer.objects.create(content_object = instance,
                                       latitude = instance.latitude,
                                       longitude = instance.longitude,
                                       location = location)
        mp.save()


def delete_marker(sender, instance, **kwargs):
    """ Delete all markers related to target model instance. """
    ct = ContentType.objects.get_for_model(instance)
    for marker in MapPointer.objects.filter(content_type=ct, object_pk=instance.pk):
        marker.delete()


if settings.USE_CACHE:
    signals.post_save.connect(update_marker_cache, sender=MapPointer)
    signals.post_delete.connect(update_marker_cache, sender=MapPointer)
