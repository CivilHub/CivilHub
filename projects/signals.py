# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action


def project_created_action(sender, instance, created, **kwargs):
    """ The creation of a project should be visible to the followers of the location. """
    if created:
        action.send(instance.creator, verb=_(u"created"),
            action_object=instance, target=instance.location)


def project_task_action(sender, instance, created, **kwargs):
    """
    The creation of groups and tasks should be visible only for participants of the 
    given project. Here we also manage topic creation and answers on the forum. 
    """
    if created:
        if hasattr(instance, 'project'):
            # A group of tasks or a discussion was created
            action_target = instance.project
        elif hasattr(instance, 'group'):
            # A task was created
            action_target = instance.group.project
        else:
            # A reply to a discussion was created
            action_target = instance.topic.project
        action.send(instance.creator, verb=_(u"created"),
        action_object=instance, target=action_target)
