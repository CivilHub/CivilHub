# -*- coding: utf-8 -*-
from itertools import chain
from actstream.models import user_stream
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from models import UserProfile


class UserActionStream(object):
    """
    Generic object for custom user stream. I've tried to use actstream's
    method to achieve similar effects, but it turned to be too problematic.
    """
    def __init__(self, user):
        """
        Initialize actstream.
        @param user django.contrib.auth.models.User instance
        """

        # Django's contrib User instance
        self.user   = user
        # Activity stream for user model
        self.stream = user_stream(self.user)
        # User object content type
        self.content_type = ContentType.objects.get_for_model(self.user)
        # User object ID
        self.object_id    = self.user.pk
        # User profile content type
        self.profile_type = ContentType.objects.get_for_model(self.user.profile)
        # User profile ID
        self.profile_id   = self.user.profile.pk


    def get_actions(self):
        """
        Return list of all actions related to user and his/her profile.
        """
        actor_actions  = self.actor_actions()
        target_actions = self.target_actions()

        return list(chain(actor_actions, target_actions))


    def actor_actions(self):
        """
        Returns all actions where user is actor.
        """
        actions = self.stream.filter(actor_content_type=self.content_type)
        actions = actions.filter(actor_object_id=self.object_id)

        return actions


    def target_actions(self):
        """
        Returns all actions where user is target. It is necessary because we
        use UserProfile instead of pure django's User object, and this is 
        the place when we link profile actions with user's stream.
        """
        user_actions = self.stream.filter(target_content_type=self.content_type)
        user_actions = user_actions.filter(target_object_id=self.object_id)
        prof_actions = self.stream.filter(target_content_type=self.profile_type)
        prof_actions = prof_actions.filter(target_object_id=self.profile_id)

        return list(chain(user_actions, prof_actions))
