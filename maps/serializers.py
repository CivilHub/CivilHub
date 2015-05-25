# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.utils.timesince import timesince
from .models import MapPointer


class MapPointerSerializer(serializers.ModelSerializer):
    """
    Serializer for map pointer.
    """
    class Meta:
        model = MapPointer
        exclude = ('id',)


class MapClusterSerializer(serializers.Serializer):
    """ Serializer for clusters. """
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    counter = serializers.IntegerField()


class MapObjectSerializer(serializers.ModelSerializer):
    """
    This serializer takes map pointer and related object and presents
    data in fixed format to display in map dialog.
    """
    lat = serializers.FloatField(source='latitude')
    lng = serializers.FloatField(source='longitude')
    content_object = serializers.SerializerMethodField('get_content_object')
    
    class Meta:
        model = MapPointer
        fields = ('lat', 'lng', 'content_object',)

    def get_content_object(self, obj):
        if obj.content_object is None:
            return {}

        tmpobj = {
            'id': obj.content_object.pk,
            'title': obj.content_object.__unicode__(),
            'url': obj.content_object.get_absolute_url(),
            'type': obj.content_object._meta.verbose_name,
            'desc': obj.content_object.get_description(),
            'date': timesince(obj.content_object.date_created),
        }

        # check if object is project-related
        if hasattr(obj.content_object.creator, 'profile'):
            tmpobj.update({
                'profile': obj.content_object.creator.profile,
                'img': obj.content_object.creator.profile.thumbnail_medium(),
                'user': obj.content_object.creator.get_full_name(),
                'profile': obj.content_object.creator.profile.get_absolute_url(),
            })
        else:
            # it is
            tmpobj.update({
                'profile': obj.content_object.creator,
                'img': obj.content_object.creator.thumbnail_medium(),
                'user': obj.content_object.creator.user.get_full_name(),
                'profile': obj.content_object.creator.get_absolute_url(),
            })

        # only for locations
        if hasattr(obj.content_object, 'kind'):
            print self.context
            usr = self.context['request'].user
            tmpobj['followers'] = obj.content_object.users.count()
            tmpobj['followed'] = usr in obj.content_object.users.all()

        return tmpobj