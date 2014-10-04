from .models import MapPointer

def create_marker(sender, instance, created, **kwargs):
    """ Create map marker for new model instance. """
    if created:
        if instance.latitude and instance.longitude:
            mp = MapPointer.objects.create(content_object = instance,
                                           latitude = instance.latitude,
                                           longitude = instance.longitude)
            mp.save()