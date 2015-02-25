# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType


class SearchResultsSerializer(serializers.Serializer):
    """ Serializer dla rezultatów wyszukiwania. """
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
    """ Paginacja wyników wyszukiwania. """
    class Meta:
        object_serializer_class = SearchResultsSerializer


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer umożliwiający pobieranie id typu zawartości na podstawie nazwy
    aplikacji/modelu i vice-versa. Przydatne kiedy chcemy ustalić typ zawartości
    dla modeli relacyjnych (komentarze, zakładki itp.).
    """
    class Meta:
        model = ContentType