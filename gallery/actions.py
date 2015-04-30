# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from actstream.actions import action

from notifications.models import notify


def created_gallery(user, instance):
    """ Send action about new gallery. Takes ContentObjectGallery as argument.
    """
    verb = _(u"created gallery")
    publisher = instance.published_in
    if publisher is None:
        action.send(user, verb=verb, action_object=instance)
    action.send(user, verb=verb, action_object=instance, target=publisher)
    if hasattr(publisher, 'creator'):
        target_user = publisher.creator
    elif hasattr(publisher, 'author'):
        target_user = publisher.author
    if target_user == user:
        return True
    notify(user, target_user,
           verb=verb,
           key="gallery",
           action_object=instance,
           action_target=publisher)


def uploaded_picture(instance):
    """ Send information about new picture in existing gallery.
    """
    verb = _(u"uploaded picture")
    action.send(instance.uploaded_by,
                verb=verb,
                action_object=instance,
                target=instance.gallery)
