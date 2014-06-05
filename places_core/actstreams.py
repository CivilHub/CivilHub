# -*- coding: utf-8 -*-
#
# W tym pliku znajdują się tzw. 'action hooki' dla activity stream.
# Rozszerzyłem ich działanie w ten sposób, że są również odpowiedzialne
# za zwiększanie punktacji użytkownika przyznawanej za wykonywane
# działania.
#
from django.db.models.signals import post_save
from actstream import action
from locations.models import Location
from ideas.models import Idea
from polls.models import Poll
from blog.models import News
from topics.models import Discussion, Entry


def create_place_action_hook(sender, instance, created, **kwargs):
    """
    Action hook for activity stream when new place is created
    TODO - move it to more appropriate place.
    """
    if created:
        instance.users.add(instance.creator)
        action.send(instance.creator, action_object=instance, verb='created')


post_save.connect(create_place_action_hook, sender=Location)


def create_object_action_hook(sender, instance, created, **kwargs):
    """
    Poinformuj o utworzeniu nowego obiektu. Można podłączyć wywołanie
    tego zdarzenie do każdego obiektu, który posiada pola 'creator'
    oraz 'location' - tzn. do modułów dziedziczących z lokacji.
    """
    if created:
        action.send(
            instance.creator,
            action_object = instance,
            verb = 'created',
            target = instance.location
        )


post_save.connect(create_object_action_hook, sender=Idea)
post_save.connect(create_object_action_hook, sender=Poll)
post_save.connect(create_object_action_hook, sender=News)
post_save.connect(create_object_action_hook, sender=Discussion)


def answer_discussion_action_hook(sender, instance, created, **kwargs):
    """
    Action hook to notice users about answers in their discussions.
    This hook is fired up anytime someone post answer on discussion.
    """
    pass


post_save.connect(answer_discussion_action_hook, sender=Entry)
