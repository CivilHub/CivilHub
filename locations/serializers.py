# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from .models import Location


class MapLocationSerializer(serializers.ModelSerializer):
    """ Prosty serializer lokalizacji dla mapy. """
    id = serializers.Field(source='pk')
    content_type = serializers.SerializerMethodField('get_content_type')
    object_pk = serializers.SerializerMethodField('get_object_pk')

    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude',)


class SimpleLocationSerializer(serializers.ModelSerializer):
    """
    Simple location serializer for mobile API. Allows to list, add and manage
    location objects in database. Provides standard CRUD operations set.
    """
    class Meta:
        model = Location


class LocationListSerializer(serializers.ModelSerializer):
    """
    Serializer do wyświetlenia w widokach listy, zawierający nazwę lokacji, 
    odnośnik bezpośredni i podstawowe informacje.
    """
    id = serializers.Field(source='pk')
    name = serializers.CharField(max_length=64)
    slug = serializers.SlugField(max_length=64)
    followed = serializers.SerializerMethodField('check_followed')

    def check_followed(self, obj):
        user = self.context['view'].request.user
        if user.is_authenticated() and user in obj.users.all():
            return True
        return False

    class Meta:
        model = Location
        fields = ('id', 'name', 'slug', 'followed',)
