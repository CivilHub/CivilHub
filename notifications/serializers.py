# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.core import serializers as dj_serializers
from django.utils.translation import ugettext as _

from rest_framework import serializers

from userspace.serializers import UserDetailSerializer

from .models import Notification


def serializer_object(obj):
    """
    Serialize object instcane via native Django seraializer and return as JSON.
    """
    if obj is None:
        return None
    data = json.loads(dj_serializers.serialize('json', [obj,]))[0]
    if hasattr(obj, 'get_absolute_url'):
        data['url'] = obj.get_absolute_url()
    return data


class NotificationSerializer(serializers.ModelSerializer):
    """ Serializer for notification model. It is meant to be read-only. """
    actor = serializers.SerializerMethodField('get_actor_data')
    action_verb = serializers.SerializerMethodField('get_action_verb')
    action_object = serializers.SerializerMethodField('get_action_object')
    action_target = serializers.SerializerMethodField('get_action_target')
    action_url = serializers.SerializerMethodField('get_action_url')
    is_new = serializers.Field(source='is_new')

    def get_actor_data(self, obj):
        serializer = UserDetailSerializer(obj.action_actor)
        return serializer.data

    def get_action_verb(self, obj):
        if obj.action_verb is None:
            return ""
        elif obj.action_verb == 'commented your':
            obj_name = " " + obj.action_target._meta.verbose_name.title()
            return _(u"commented your") + obj_name
        elif obj.action_verb == 'voted for your idea':
            if obj.action_object.status == 1:
                return _(u"voted up for your idea")
            else:
                return _(u"voted down for your idea")
        return _(obj.action_verb)

    def get_action_object(self, obj):
        return serializer_object(obj.action_object)

    def get_action_target(self, obj):
        return serializer_object(obj.action_target)

    def get_action_url(self, obj):
        """ Try to find most appropriate url for this kind of notification. """
        # If there is no better match, point to actor profile url
        action_url = obj.action_actor.profile.get_absolute_url()
        # Fallback if action_target is undefined:
        if obj.action_object is not None:
            if hasattr(obj.action_object, 'get_absolute_url'):
                action_url = obj.action_object.get_absolute_url()
        # And most preferred option - get url from action target
        if obj.action_target is not None:
            if hasattr(obj.action_target, 'get_absolute_url'):
                action_url = obj.action_target.get_absolute_url()
        return action_url

    class Meta:
        model = Notification
        fields = ('created_at', 'checked_at', 'is_new', 'actor', 'action_verb',
                  'action_url', 'key', 'action_object', 'action_target',)


class NotificationSimpleSerializer(serializers.ModelSerializer):
    """ This is simplest serializer to present on lists. """
    class Meta:
        model = Notification
