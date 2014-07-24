# -*- coding: utf-8 -*-
#
# W tym pliku znajdują się tzw. 'action hooki' dla activity stream.
# Rozszerzyłem ich działanie w ten sposób, że są również odpowiedzialne
# za zwiększanie punktacji użytkownika przyznawanej za wykonywane
# działania.
#
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from actstream import action
from actstream.actions import follow
from userspace.models import UserProfile
from locations.models import Location
from comments.models import CustomComment as Comment
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
        action.send(instance.creator, action_object=instance, verb=_('created'))
        instance.users.add(instance.creator)
        instance.creator.profile.mod_areas.add(instance)
        follow(instance.creator, instance, actor_only = False)


post_save.connect(create_place_action_hook, sender=Location)


def create_object_action_hook(sender, instance, created, **kwargs):
    """
    Poinformuj o utworzeniu nowego obiektu. Można podłączyć wywołanie
    tego zdarzenie do każdego obiektu, który posiada pola 'creator'
    oraz 'location' - tzn. do modułów dziedziczących z lokacji.
    """
    if created:
        prof = UserProfile.objects.get(user=instance.creator)
        prof.rank_pts += 5
        prof.save()
        action.send(
            instance.creator,
            action_object = instance,
            verb = _('created'),
            target = instance.location
        )


post_save.connect(create_object_action_hook, sender=Idea)
post_save.connect(create_object_action_hook, sender=News)


def create_raw_object_action_hook(sender, instance, created, **kwargs):
    """
    Ten zaczep jest wykorzystywany przez modele, które użytkownik
    może tworzyć, ale nie są punktowane (np. dyskusje). Mogą z niego
    korzystać wszystkie obiekty, które mają pola 'creator' oraz 'location'.
    """
    if created:
        action.send(
            instance.creator,
            action_object = instance,
            verb = _('created'),
            target = instance.location
        )


post_save.connect(create_object_action_hook, sender=Discussion)
post_save.connect(create_object_action_hook, sender=Poll)


def answer_discussion_action_hook(sender, instance, created, **kwargs):
    """
    Action hook to notice users about answers in their discussions.
    This hook is fired up anytime someone post answer on discussion.
    """
    pass


post_save.connect(answer_discussion_action_hook, sender=Entry)


def comment_action_hook(sender, instance, created, **kwargs):
    """
    Action hook dla komentarzy - poinformuj innych o tym, że komentarz
    został utworzony ora z zwiększ odpowiednio liczbę punktów użytkownika.
    """
    if created:
        prof = UserProfile.objects.get(user=instance.user)
        prof.rank_pts += 3
        prof.save()
        action.send(
            instance.user,
            action_object = instance.content_object,
            verb = _('commented'),
            comment = instance.comment,
            comment_url = instance.content_object.get_absolute_url() + '#comment-' + str(instance.pk)
        )


post_save.connect(comment_action_hook, sender=Comment)
