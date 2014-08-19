# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from .models import Location


class MapLocationSerializer(serializers.ModelSerializer):
    """
    Prosty serializer dla mapy. Przechowuje tylko podstawowe informacje o lo-
    kalizacji, czyli id, długość oraz szerokość geograficzną i typ zawartości
    (żeby sobie później ułatwić doczytywanie/segregowanie obiektów na mapie).
    Tylko zapytania typu GET! Serializers niejako sztucznie dopasowuje infor-
    macje o obiekcie na wzór obiektów z mapy (markerów), dając do dyspozycji
    ten sam szkielet modelu do Backbone.
    
    Umożliwia wyszukiwanie na podstawie kodu kraju (country_code), np:
    `?code=pl`
    zwróci wszystkie lokalizacje w Polsce.
    """
    content_type = serializers.SerializerMethodField('get_content_type')
    object_pk = serializers.SerializerMethodField('get_object_pk')

    def get_object_pk(self, obj):
        """
        Funkcja konwertuje pk obiektu na postać ciągu znaków dla potrzeb
        front-endowych aplikacji.
        """
        return str(obj.pk)

    def get_content_type(self, obj):
        return ContentType.objects.get_for_model(Location).pk

    class Meta:
        model = Location
        fields = ('latitude', 'longitude', 'content_type', 'object_pk',)


class SimpleLocationSerializer(serializers.ModelSerializer):
    """
    Simple location serializer for mobile API. Allows to list, add and manage
    location objects in database. Provides standard CRUD operations set.
    """
    class Meta:
        model = Location


class LocationListSerializer(serializers.ModelSerializer):
    """
    Prosty serializer do wyświetlenia w widokach listy, zawierający nazwę loka-
    cji, odnośnik bezpośredni i podstawowe informacje.
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
