# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import SocialProject, TaskGroup, Task


class ProjectActionSerializer(serializers.ModelSerializer):
    """ Returns basic information about the object to be used in activities. """
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = SocialProject
        fields = ('id', 'name', 'url',)


class TaskGroupActionSerializer(serializers.ModelSerializer):
    """ As above, but this time it referes to a group of tasks. """
    url = serializers.SerializerMethodField('get_object_url')

    class Meta:
        model = TaskGroup
        fields = ('id', 'name', 'url',)

    def get_object_url(self, obj):
        return obj.project.get_absolute_url()


class TaskActionSerializer(serializers.ModelSerializer):
    """ A serializer for actions connected with the task. """
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = Task
        fields = ('id', 'name', 'url',)
