# -*- coding: utf-8 -*-
from .models import MapPointer


def create_marker(sender, instance, created, **kwargs):
    """ Create marker for new created object. Mark it's location approprietly
        if it is location or object related to location. It needs models with
        latitude and longitude fields to work, so it's mostly useful for
        locations.
    """
    if not hasattr(instance, 'latitude') or not hasattr(instance, 'longitude'):
        return False

    lat = instance.latitude
    lng = instance.longitude

    # Try to remove obsolete markers if lat or lng has changed
    if not created:
        for m in MapPointer.objects.for_model(instance):
            if m.latitude != lat or m.longitude != lng:
                m.delete()

    mp = MapPointer.objects.create_for_object(instance, lat, lng)
