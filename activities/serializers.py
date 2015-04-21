# -*- coding: utf-8 -*-
import json

from django.core.serializers import serialize
from django.template.defaultfilters import timesince

from actstream.models import Action
from rest_framework import serializers

from places_core.helpers import truncatehtml
from userspace.serializers import UserDetailSerializer


content_objects = ['discussion', 'idea', 'news', 'poll', 'socialproject', ]


def serialize_content_object(instance):
    if instance is None:
        return instance
    data = json.loads(serialize('json', [instance, ]))[0]
    data['name'] = instance.__unicode__()
    return data


class WrongModelInstance(Exception):

    pass


class ActionObjectSerializer(serializers.Serializer):
    """
    Serializer for content objects, such as ideas or blog entries. It is made
    to present data in common way.
    """
    id = serializers.Field(source='id')
    content_type = serializers.SerializerMethodField('get_content_type')
    author = serializers.SerializerMethodField('get_author')
    title = serializers.SerializerMethodField('get_title')
    description = serializers.SerializerMethodField('get_description')
    location = serializers.SerializerMethodField('get_location')
    url = serializers.SerializerMethodField('get_url')
    image = serializers.SerializerMethodField('get_image')

    def get_content_type(self, obj):
        return {
            'name': obj._meta.verbose_name.title(),
            'type': obj._meta.model_name,
        }

    def get_author(self, obj):
        if not hasattr(obj, 'creator'):
            return None
        serializer = UserDetailSerializer(obj.creator)
        return serializer.data

    def get_title(self, obj):
        if obj._meta.model_name == 'locationgalleryitem':
            return obj.name
        return obj.__unicode__()

    def get_description(self, obj):
        if obj._meta.model_name == 'idea':
            desc = obj.description
        elif obj._meta.model_name == 'news':
            desc = obj.content
        elif obj._meta.model_name == 'discussion':
            desc = obj.intro
        elif obj._meta.model_name == 'poll':
            desc = obj.question
        elif obj._meta.model_name == 'socialproject':
            desc = obj.description
        elif obj._meta.model_name == 'locationgalleryitem':
            desc = '<img src="{}" alt="{}">'.format(obj.url(), obj.name)
        else:
            desc = ""
        return truncatehtml(desc, 200)

    def get_location(self, obj):
        if hasattr(obj, 'location'):
            return serialize_content_object(obj.location)
        return None

    def get_url(self, obj):
        if hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()
        return None

    def get_image(self, obj):
        if not hasattr(obj, 'thumbnail'):
            return None
        image_data = {
            'url': obj.image_url,
            'thumbnail': obj.thumbnail,
        }
        if hasattr(obj, 'has_default_image'):
            image_data['is_default'] = obj.has_default_image
        if hasattr(obj, 'retina_thumbnail'):
            image_data['retina_thumbnail'] = obj.retina_thumbnail
        return image_data


class ActionTargetSerializer(serializers.Serializer):
    """
    Simple serializer for action target.
    """
    name = serializers.Field(source='__unicode__')
    kind = serializers.SerializerMethodField('get_content_type')
    url = serializers.SerializerMethodField('get_url')

    def get_content_type(self, obj):
        return {
            'name': obj._meta.verbose_name.title(),
            'type': obj._meta.model_name,
        }

    def get_url(self, obj):
        if hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()
        return None


class ActionSerializer(serializers.ModelSerializer):
    """
    Serializer meant to be read-only, presenting detailed info about actions.
    """
    actor = serializers.SerializerMethodField('get_actor_data')
    action_object = serializers.SerializerMethodField('get_action_object')
    action_target = serializers.SerializerMethodField('get_action_target')

    def get_actor_data(self, obj):
        if obj.actor is None:
            return None
        serializer = UserDetailSerializer(obj.actor)
        return serializer.data

    def get_action_object(self, obj):
        if not obj.action_object:
            return None
        try:
            serializer = ActionObjectSerializer(obj.action_object)
            return serializer.data
        except WrongModelInstance:
            return serialize_content_object(obj.action_object)

    def get_action_target(self, obj):
        if not obj.target:
            return None
        serializer = ActionTargetSerializer(obj.target)
        return serializer.data

    class Meta:
        model = Action
        fields = ('id', 'actor', 'timestamp', 'verb', 'action_object',
                  'action_target')
