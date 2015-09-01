# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from locations.serializers import LocationListSerializer
from userspace.serializers import UserDetailSerializer

from .models import Idea, Vote


class IdeaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea


class IdeaDetailSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField('get_userdata')
    location = serializers.SerializerMethodField('get_location')
    status = serializers.SerializerMethodField('get_status')
    image = serializers.SerializerMethodField('get_image')

    def get_userdata(self, obj):
        return UserDetailSerializer(obj.creator).data

    def get_location(self, obj):
        return LocationListSerializer(obj.location).data

    def get_status(self, obj):
        return obj.get_status_display()

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Idea


class VoteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote


class VoteDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_userdata')
    status = serializers.Field(source='get_status_display')

    def get_userdata(self, obj):
        return UserDetailSerializer(obj.user).data

    class Meta:
        model = Vote
