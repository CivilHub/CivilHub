# -*- coding: utf-8 -*-
from django.db import IntegrityError

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

    if not lat or not lng:
        return

    # Try to remove obsolete markers if lat or lng has changed
    for m in MapPointer.objects.for_model(instance):
        m.delete()

    try:
        mp = MapPointer.objects.create_for_object(instance, lat, lng)
    except IntegrityError:
        mp = MapPointer.objects.for_model(instance).first()

    return mp
