# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType


class SearchResultsSerializer(serializers.Serializer):
    """ A serializer for search results. """
    name = serializers.SerializerMethodField('get_verbose_name')
    content_type = serializers.SerializerMethodField('get_content_type')
    object_pk = serializers.Field(source='pk')

    def get_verbose_name(self, obj):
        if obj.object is None:
            return ''
        return obj.object.__unicode__()

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(obj.object).pk


class PaginatedSearchSerializer(PaginationSerializer):
    """ Search results pagination. """
    class Meta:
        object_serializer_class = SearchResultsSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    A serializer that allows to download id types of content based on
    the application/model name and vice-versa. Useful when we want to establish
    the type of content for relation models (comments, bookmarks etc.).
    """
    class Meta:
        model = ContentType


class ImagableModelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    def get_image(self, obj):
        if obj.has_default_image:
            return False
        return obj.image_url
