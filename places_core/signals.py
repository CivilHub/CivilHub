from django.core import cache
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from locations.models import Location
from blog.models import News
from topics.models import Discussion
from polls.models import Poll
from ideas.models import Idea


redis_cache = cache.get_cache('redis')


def update_cached_items(sender, instance, created, **kwargs):
    """ 
    Update cached items for location set so there will be no delay between
    creating content object and displaying it.
    """
    postfix = None

    if isinstance(instance, News):
        postfix = '_news'
    elif isinstance(instance, Idea):
        postfix = '_ideas'
    elif isinstance(instance, Discussion):
        postfix = '_forum'
    elif isinstance(instance, Poll):
        postfix = '_polls'

    if postfix is None or not hasattr(instance, 'location'):
        return False

    ct = ContentType.objects.get_for_model(instance)
    qs = ct.get_all_objects_for_this_type() \
        .filter(location__pk__in=instance.location.get_children_id_list())
    qs = ct.get_all_objects_for_this_type().filter(location=instance.location)

    redis_cache.set(instance.location.slug+postfix, qs)


post_save.connect(update_cached_items, sender=News)
post_save.connect(update_cached_items, sender=Idea)
post_save.connect(update_cached_items, sender=Poll)
post_save.connect(update_cached_items, sender=Discussion)
