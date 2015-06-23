# -*- coding: utf-8 -*-
from rest_framework import serializers

from userspace.serializers import UserDetailSerializer

from .models import Blessing


class BlessSerializer(serializers.ModelSerializer):
    """ Simple serializer for our recommendation model.
    """
    class Meta:
        model = Blessing


class BlessDetailSerializer(serializers.ModelSerializer):
    """ This serializer is meant to read and list functions and presents
        detailed info about selected Blessing along with detailed user info.
    """
    user = serializers.SerializerMethodField('get_userdata')

    def get_userdata(self, obj):
        return UserDetailSerializer(obj.user).data

    class Meta:
        model = Blessing
