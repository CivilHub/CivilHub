# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from .models import Location, Country


class ContentObjectSerializer(serializers.Serializer):
    """
    Proxy dla obiektów wyciąganych z listy relacji wybranej lokalizacji.
    Metoda sama serializuje dane, ta klasa potrzebna jest, aby połączyć nasz
    skrypt z REST API poprzez restowe APIView oraz PaginationSerializer.
    Oczywiście działa tylko read-only.
    """
    type = serializers.Field(source='type')
    name = serializers.Field(source='name')
    slug = serializers.Field(source='slug')
    ct = serializers.Field(source='ct')
    pk = serializers.Field(source='pk')
    url = serializers.Field(source='url')
    title = serializers.Field(source='title')
    image = serializers.Field(source='image')
    thumbnail = serializers.Field(source='thumbnail')
    retina_thumbnail = serializers.Field(source='retina_thumbnail')
    meta = serializers.Field(source='meta')
    creator = serializers.Field(source='creator')
    category = serializers.Field(source='category')
    location = serializers.Field(source='location')
    description = serializers.Field(source='description')
    date_created = serializers.Field(source='date_created')


class ContentPaginatedSerializer(PaginationSerializer):
    """
    Nakładka pozwalająca nam wypuścić listę obiektów w
    lokalizacji przez paginowalne APIView z Rest Framework.
    """
    class Meta:
        object_serializer_class = ContentObjectSerializer


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
    name = serializers.Field(source='__unicode__')
    slug = serializers.SlugField(max_length=64)
    followed = serializers.SerializerMethodField('check_followed')

    def check_followed(self, obj):
        view_context = self.context.get('view')
        if view_context is not None:
            user = view_context.request.user
            if user.is_authenticated() and user in obj.users.all():
                return True
        return False

    class Meta:
        model = Location
        fields = ('id', 'name', 'slug', 'followed',)


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer umożliwiający łatwiejsze namierzanie lokalizacji użytkownika.
    Dla aplikacji mobilnej raczej bardziej przydatne będą natywne funkcje
    geolokacji, ale dla porządku to też puszczam przez REST.
    """
    capital = serializers.SerializerMethodField('get_capital_location')

    def get_capital_location(self, obj):
        capital = obj.get_capital()
        serializer = LocationListSerializer(capital)
        return serializer.data

    class Meta:
        model = Country
