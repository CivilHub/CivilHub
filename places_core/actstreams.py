# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from actstream import action
from ideas.models import Idea

def idea_action_handler(sender, instance, created, **kwargs):
    if created:
        action.send(
            instance.creator,
            action_object = instance,
            verb = 'created',
            target = instance.location
        )
    
post_save.connect(idea_action_handler, sender=Idea)