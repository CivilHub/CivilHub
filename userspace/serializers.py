# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from bookmarks.models import Bookmark


class UserAuthSerializer(serializers.ModelSerializer):
    """
    Serializer używany przy autoryzacji użytkowników logujących się przez api
    zewnętrznych dostawców.
    """
    token = serializers.Field(source='auth_token')

    class Meta:
        model = User
        fields = ('id', 'token',)


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer dla zakładek użytkownika.
    """
    key = serializers.CharField(max_length=16, required=False)
    
    class Meta:
        model = Bookmark