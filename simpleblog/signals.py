# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action


def blog_entry_created_action(sender, instance, created, **kwargs):
    """
    Notify followers about new blog entries related to some other objects.
    """
    if not created:
        return True
    if instance.content_object is None:
        action.send(instance.author,
                    action_object=instance,
                    verb=_('created'))
    else:
        action.send(instance.author,
                    action_object=instance,
                    verb=_('created'),
                    target=instance.content_object)
