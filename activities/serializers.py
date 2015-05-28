# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.template.defaultfilters import timesince
from django.utils.translation import ugettext as _

from actstream.models import Action
from rest_framework import serializers

from comments.models import CustomComment
from places_core.helpers import truncatehtml
from userspace.serializers import UserDetailSerializer

content_objects = ['discussion',
                   'idea',
                   'news',
                   'poll',
                   'socialproject',
                   'blogentry', ]


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
    date_created = serializers.SerializerMethodField('get_creation_date')
    comment_count = serializers.SerializerMethodField('get_comment_count')

    def get_creation_date(self, obj):
        if hasattr(obj, 'date_created'):
            return obj.date_created
        return None

    def get_content_type(self, obj):
        return {
            'id': ContentType.objects.get_for_model(obj).pk,
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
        elif obj._meta.model_name == 'socialforumentry':
            return obj.topic.__unicode__()
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
        elif obj._meta.model_name == 'blogentry':
            desc = obj.content
        elif obj._meta.model_name == 'vote' \
            or obj._meta.model_name == 'commentvote':
            if obj.vote:
                class_name = 'alert-success'
                label_text = _(u"Voted yes")
            else:
                class_name = 'alert-danger'
                label_text = _(u"Voted no")
            return u'<div class="alert {}">{}</div>'.format(class_name,
                                                            label_text)
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
        image_data = {'url': obj.image_url, 'thumbnail': obj.thumbnail, }
        if hasattr(obj, 'has_default_image'):
            image_data['is_default'] = obj.has_default_image
        if hasattr(obj, 'retina_thumbnail'):
            image_data['retina_thumbnail'] = obj.retina_thumbnail
        return image_data

    def get_comment_count(self, obj):
        return len(CustomComment.objects.for_model(obj))


class ActionTargetSerializer(serializers.Serializer):
    """
    Simple serializer for action target.
    """
    name = serializers.SerializerMethodField('get_name')
    kind = serializers.SerializerMethodField('get_content_type')
    url = serializers.SerializerMethodField('get_url')

    def get_name(self, obj):
        if obj._meta.model_name == 'user':
            return obj.get_full_name()
        elif obj._meta.model_name == 'locationgalleryitem':
            return obj.name
        return obj.__unicode__()

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
    verb = serializers.SerializerMethodField('get_verb')

    def get_actor_data(self, obj):
        if obj.actor is None:
            return None
        serializer = UserDetailSerializer(obj.actor)
        return serializer.data

    def get_action_object(self, obj):
        if not obj.action_object:
            return None
        serializer = ActionObjectSerializer(obj.action_object)
        return serializer.data

    def get_action_target(self, obj):
        ct = obj.target_content_type
        pk = obj.target_object_id
        if not ct or not pk:
            return None
        target = ct.get_object_for_this_type(pk=pk)
        serializer = ActionTargetSerializer(target)
        return serializer.data

    def get_verb(self, obj):
        return _(obj.verb)

    def to_representation(self, data):
        data = data.filter(user=self.request.user, edition__hide=False)
        return super(ActionSerializer, self).to_representation(data)

    def __init__(self, *args, **kwargs):
        self.filter = kwargs.get('filter')
        super(ActionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Action
        fields = ('id', 'actor', 'timestamp', 'verb', 'action_object',
                  'action_target')
