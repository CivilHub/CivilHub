# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import SocialProject, TaskGroup, Task


class ProjectActionSerializer(serializers.ModelSerializer):
    """ Zwraca podstawowe informacje o obiekcie do wykorzystania w activities. """
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = SocialProject
        fields = ('id', 'name', 'url',)


class TaskGroupActionSerializer(serializers.ModelSerializer):
    """ J/w, z tym, że ma zastosowanie do grup zadań. """
    url = serializers.SerializerMethodField('get_object_url')

    class Meta:
        model = TaskGroup
        fields = ('id', 'name', 'url',)

    def get_object_url(self, obj):
        return obj.project.get_absolute_url()


class TaskActionSerializer(serializers.ModelSerializer):
    """ Serializer dla akcji powiązanych z zadaniem. """
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = Task
        fields = ('id', 'name', 'url',)
