# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from actstream import action
from ideas.models import Idea
from polls.models import Poll
from blog.models import News


def create_object_action_handler(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.creator,
            action_object = instance,
            verb = 'created',
            target = instance.location
        )


post_save.connect(create_object_action_handler, sender=Idea)
post_save.connect(create_object_action_handler, sender=Poll)
#post_save.connect(create_object_action_handler, sender=News)
