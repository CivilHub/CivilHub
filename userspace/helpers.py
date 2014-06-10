# -*- coding: utf-8 -*-
from itertools import chain
from actstream.models import Action, user_stream
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from models import UserProfile


class UserActionStream(object):
    """
    Generic object for custom user stream. I've tried to use actstream's
    method to achieve similar effects, but it turned to be too problematic.
    
    This class manages user's actions, not his action streams (despite it's
    name). It is included to show and count actions performed by user, related
    to user and his/her profile.
    """
    def __init__(self, user):
        """
        Initialize actstream.
        @param user django.contrib.auth.models.User instance
        """

        # Django's contrib User instance
        self.user = user
        # User object content type
        self.content_type = ContentType.objects.get_for_model(self.user)
        # User object ID
        self.object_id    = self.user.pk
        # User profile content type
        self.profile_type = ContentType.objects.get_for_model(self.user.profile)
        # User profile ID
        self.profile_id   = self.user.profile.pk
        # Custom activity queryset
        self.stream       = self._get_queryset()


    def _get_queryset(self):
        """
        Get custom Action object queryset to replace built-in Activity Stream
        mechanism of fetching object-related actions.
        """
        # Actions for user
        actor    = Action.objects.filter(actor_content_type=self.content_type)
        actor    = actor.filter(actor_object_id=self.object_id)
        obj      = Action.objects.filter(action_object_content_type=self.content_type)
        obj      = obj.filter(action_object_object_id=self.object_id)
        target   = Action.objects.filter(target_content_type=self.content_type)
        target   = target.filter(target_object_id=self.object_id)
        # Actions for user profile
        p_actor  = Action.objects.filter(actor_content_type=self.profile_type)
        p_actor  = p_actor.filter(actor_object_id=self.profile_id)
        p_obj    = Action.objects.filter(action_object_content_type=self.profile_type)
        p_obj    = p_obj.filter(action_object_object_id=self.profile_id)
        p_target = Action.objects.filter(target_content_type=self.profile_type)
        p_target = p_target.filter(target_object_id=self.profile_id)

        self.actor_related  = actor  | p_actor
        self.obj_related    = obj    | p_obj
        self.target_related = target | p_target

        return actor | obj | target | p_actor | p_obj | p_target


    def get_actions_by_type(self, stream, content_type=None):
        """
        Get only actions related to given content type - e.g. only Ideas.
        
        Previously filtered stream must be provided as mandatory argument.
        This is where we start further filtering.
        
        If 'content_type' is provided in form of 'app_name.model_name' string,
        return only actions related to search item. Otherwise function returns
        all user actions.
        """
        if not content_type:
            return stream

        app_name, model_name = content_type.split('.')
        content_type = ContentType.objects.get_by_natural_key(app_name,
                                                              model_name)

        actor_actions  = stream.filter(actor_content_type=content_type)
        target_actions = stream.filter(target_content_type=content_type)
        object_actions = stream.filter(action_object_content_type=content_type)

        return actor_actions | target_actions | object_actions


    def get_actions(self, content_type=None, action_type=None):
        """
        Return django queryset containing list of all actions related
        to user and his/her profile.
        
        If 'content_type' is provided, actions will be filtered to only this
        related to given content type (in form of "app_name.model_name"
        string.
        
        If 'action_type' is provided, actions will be filtered that results
        will only contain actions where user acted as provided actstream
        element (e.g. 'actor', 'object' or 'target').
        """
        stream = self.stream

        if action_type == 'actor':
            stream = self.actor_actions()
        if action_type == 'object':
            stream = self.object_actions()
        if action_type == 'target':
            stream = self.target_actions()

        return self.get_actions_by_type(stream, content_type)


    def actor_actions(self):
        """
        Returns all actions where user or profile is actor.
        """
        return self.actor_related


    def object_actions(self):
        """
        Returns all actions where user or profile acts as action object.
        This is highly unlikely but not impossible.
        """
        return self.object_related


    def target_actions(self):
        """
        Returns all actions where user or profile is target.
        """
        return self.target_related
