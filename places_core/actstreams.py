# -*- coding: utf-8 -*-
#
# Here, the so-called 'action hooks' for the activity stream are located.
# I have expanded their usage so that they are also responsible for increasing
# user points that are awarded for action.
#
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from actstream import action
from actstream.actions import follow

from blog.models import News
from comments.models import CustomComment
from ideas.models import Idea
from locations.models import Location
from notifications.models import notify
from polls.models import Poll
from topics.models import Discussion, Entry
from userspace.models import UserProfile


def create_place_action_hook(sender, instance, created, **kwargs):
    """
    Action hook for activity stream when new place is created
    TODO - move it to more appropriate place.
    """
    if created:
        action.send(instance.creator, action_object=instance, verb=_('created'))
        instance.users.add(instance.creator)
        instance.creator.profile.mod_areas.add(instance)
        follow(instance.creator, instance, actor_only = False)
post_save.connect(create_place_action_hook, sender=Location)


def create_object_action_hook(sender, instance, created, **kwargs):
    """
    Inform about the creation of a new object. It is possible
    to plugg evocation of this idea for each object that has the field
    'creator' and 'location' - i.e. for modules that inherit from a location.
    """
    if not created:
        return True
    prof = UserProfile.objects.get(user=instance.creator)
    prof.rank_pts += 5
    prof.save()
    action.send(
        instance.creator,
        action_object = instance,
        verb = _(u"created"),
        target = instance.location
    )
    # This way author will be notified about comments etc.
    follow(instance.creator, instance)
post_save.connect(create_object_action_hook, sender=Idea)
post_save.connect(create_object_action_hook, sender=News)


def create_raw_object_action_hook(sender, instance, created, **kwargs):
    """
    This anchor is used by models that the user can create but they are
    not single-pointed (e.g. discussions). All objects that have the field
    'creator' and 'location' can make use of it.
    """
    if created:
        action.send(
            instance.creator,
            action_object = instance,
            verb = _(u"created"),
            target = instance.location
        )
        # This way author will be notified about comments etc.
        follow(instance.creator, instance)
post_save.connect(create_object_action_hook, sender=Discussion)
post_save.connect(create_object_action_hook, sender=Poll)


def comment_action_hook(sender, instance, created, **kwargs):
    """
    Action hook for comments - inform other people about the fact that
    this comment was created and increase the amount of user points
    accordingly.
    """
    if not created:
        return True
    prof = UserProfile.objects.get(user=instance.user)
    prof.rank_pts += 3
    prof.save()
    # Send action for user and location activity streams
    action.send(
        instance.user,
        action_object = instance,
        target = instance.content_object,
        verb = _(u"commented"),
        comment = instance.comment,
        comment_url = instance.content_object.get_absolute_url()
    )
    # Send notification to parent comment author (if this is answer for comment)
    if instance.parent is not None:
        notify(
            instance.user,
            instance.parent.user,
            key="customcomment",
            verb=_(u"answered your comment"),
            action_object=instance,
            action_target=instance.parent
        )
post_save.connect(comment_action_hook, sender=CustomComment)
