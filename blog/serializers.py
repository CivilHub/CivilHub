# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest.serializers import TranslatedModelSerializer

from places_core.helpers import truncatehtml
from userspace.serializers import UserDetailSerializer

from .models import Category, News


class NewsCategorySerializer(TranslatedModelSerializer):
    """
    Simple serializer for Category News in Blog.
    """
    class Meta:
        model = Category
        exclude = ('slug',)


class NewsSimpleSerializer(serializers.ModelSerializer):
    """
    Simplified News object serializer for mobile API.
    """
    id = serializers.Field(source='pk')
    slug = serializers.SlugField(required=False)

    class Meta:
        model = News
        exclude = ('creator',)


class NewsDetailedSerializer(serializers.ModelSerializer):
    """
    Show detailed info about news entry.
    """
    author = serializers.SerializerMethodField('get_user_data')
    content = serializers.SerializerMethodField('get_content')
    image = serializers.Field(source='image.url')
    location = serializers.Field(source='location.__unicode__')
    url = serializers.Field(source='get_absolute_url')

    def get_user_data(self, obj):
        serializer = UserDetailSerializer(obj.creator)
        return serializer.data

    def get_content(self, obj):
        return truncatehtml(obj.content, 100)

    class Meta:
        model = News
        exclude = ('creator',)
