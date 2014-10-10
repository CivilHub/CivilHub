from locations.models import Location
from .models import MapPointer

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
