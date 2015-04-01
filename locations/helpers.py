# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from actstream.models import Action
from actstream.actions import follow, unfollow

from .models import Location


def get_most_followed(country_code=None, limit=20):
    """
    We download a list of the most often followed location. We can narrow
    the list to a certain country, to do so, we first type in the country
    and its capital city. it returns a LIST, not a QuerySet!
    """
    qs = Location.objects
    kinds = ['PPLC', 'country',]
    if country_code is None:
        return list(qs.all().order_by('-users')[:limit])
    main = list(qs.filter(country_code=country_code,
                  kind__in=kinds).order_by('kind'))
    full = list(qs.filter(country_code=country_code)\
                  .exclude(kind__in=kinds)\
                  .order_by('-users')[:limit-len(main)])
    return main + full


def move_location_contents(old_location, new_location):
    """
    This method helps us move contents between locations, mainly, if we want
    to delete one location but save contents in other one. It takes two location
    instances as arguments and move content from first to second of them.
    """
    content_sets = ['news_set', 'poll_set', 'idea_set',
                    'discussion_set', 'pictures', 'projects',]
    # Get all 'standard' contents from first location and move to second one
    for content_type in content_sets:
        for item in getattr(old_location, content_type).all():
            item.location = new_location
            item.save()
    # Find all old location followers and make them follow new place
    for user in old_location.users.all():
        unfollow(user, old_location)
        if not user in new_location.users.all():
            follow(user, new_location)
            new_location.users.add(user)
    # Find all actions where old location acts as target and bind to new location.
    # This is not really good idea, but I hope it will be sufficient.
    actions = Action.objects.filter(target_object_id=old_location.pk,
        target_content_type=ContentType.objects.get_for_model(Location))
    for action in actions:
        action.target_object_id = new_location.pk
        action.save()


def get_followers_from_location(location_pk, deep=False):
    """
    Helper that returns list of all followers from location with given ID.
    If `deep` is set to True, list includes also followers of child locations.
    We don't count superusers in results, only regular users.
    """
    location = Location.objects.get(pk=location_pk)
    followers = list(location.users.all())
    if not deep:
        return followers
    for pk in location.get_children_id_list():
        location = Location.objects.get(pk=pk)
        for user in location.users.all():
            if not user in followers:
                followers.append(user)
    return followers
