from django.db.models import signals
from django.core.cache import cache
from locations.models import Location
from .models import MapPointer
from .helpers import create_country_clusters


def update_marker_cache(sender, instance, **kwargs):
    """
    """
    count = MapPointer.objects.filter(
        location__in=instance.location.parent.get_children_id_list()).count()
    cache.set(str(instance.location.pk) + '_childlist', count)
    cache.set('allcountries', create_country_clusters())


def create_marker(sender, instance, created, **kwargs):
    """ Create map marker for new model instance. """
    if created and instance.latitude and instance.longitude:
        mp = MapPointer.objects.create(content_object = instance,
                                       latitude = instance.latitude,
                                       longitude = instance.longitude)

        if isinstance(instance, Location):
            mp.location = instance
        elif hasattr(instance, 'location'):
            mp.location = instance.location

        mp.save()


signals.post_save.connect(update_marker_cache, sender=MapPointer)
signals.post_delete.connect(update_marker_cache, sender=MapPointer)

