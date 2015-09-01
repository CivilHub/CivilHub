# -*- coding: utf-8 -*-
from rest_framework import serializers

from userspace.serializers import UserDetailSerializer
from .models import SocialProject, TaskGroup, Task


# Base serializers for mobile API

class ProjectDetailSerializer(serializers.ModelSerializer):
    """ Serializer for list and retrive views, presenting detail info.
    """
    image = serializers.SerializerMethodField('get_image')
    participants = serializers.SerializerMethodField('get_participants')
    creator = serializers.SerializerMethodField('get_creator')

    class Meta:
        model = SocialProject
        exclude = ('authors_group',)

    def get_image(self, obj):
        return obj.image.url

    def get_participants(self, obj):
        return UserDetailSerializer(obj.participants.all(), many=True).data

    def get_creator(self, obj):
        return UserDetailSerializer(obj.creator).data


class TaskGroupSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField('get_project')
    creator = serializers.SerializerMethodField('get_creator')

    class Meta:
        model = TaskGroup

    def get_project(self, obj):
        return ProjectDetailSerializer(obj.project).data

    def get_creator(self, obj):
        return UserDetailSerializer(obj.creator).data


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField('get_creator')
    group = serializers.SerializerMethodField('get_group')
    participants = serializers.SerializerMethodField('get_participants')

    class Meta:
        model = Task

    def get_creator(self, obj):
        return UserDetailSerializer(obj.creator).data

    def get_group(self, obj):
        return TaskGroupSerializer(obj.group).data

    def get_participants(self, obj):
        return UserDetailSerializer(obj.participants.all(), many=True).data


# Serializers for Activity Stream and inner website scripts.

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

