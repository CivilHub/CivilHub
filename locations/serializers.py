# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import Location, Country


class AutocompleteLocationSeraializer(serializers.ModelSerializer):
    """
    This is serializer especially for autocomplete.
    """
    value = serializers.Field(source='pk')
    label = serializers.SerializerMethodField('get_label')

    def get_label(self, obj):
        names = [obj.__unicode__(), ]
        qs = Location.objects.filter(pk__in=obj.get_parents)\
                            .order_by('-kind').values('name', )
        names = names + [x['name'] for x in qs]
        return " ".join(names)

    class Meta:
        model = Location
        fields = ('value', 'label', )


class ContentObjectSerializer(serializers.Serializer):
    """
    A proxy for objects pull from the relation list of given locations.
    The method itself does not serialize the data, this class is required
    in order to connect our script with REST API through rest APIView and
    PaginationSerializer. Of course, it is read-only.
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
    default_image = serializers.Field(source='default_image')


class ContentPaginatedSerializer(PaginationSerializer):
    """
    An overlay that allows to send a list of objects
    in a location through a paginal APIView from the Rest
    Framework.
    """
    class Meta:
        object_serializer_class = ContentObjectSerializer


class MapLocationSerializer(serializers.ModelSerializer):
    """ A simple location serializer for the map. """
    id = serializers.Field(source='pk')
    content_type = serializers.SerializerMethodField('get_content_type')
    object_pk = serializers.SerializerMethodField('get_object_pk')

    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude', )


class SimpleLocationSerializer(serializers.ModelSerializer):
    """
    Simple location serializer for mobile API. Allows to list, add and manage
    location objects in database. Provides standard CRUD operations set.
    """
    class Meta:
        model = Location


class LocationListSerializer(serializers.ModelSerializer):
    """
    A serializer that displays in the views lists that contain the name
    of the location, a direct link and basic information.
    """
    id = serializers.Field(source='pk')
    name = serializers.Field(source='__unicode__')
    slug = serializers.SlugField(max_length=64)
    followed = serializers.SerializerMethodField('check_followed')

    def check_followed(self, obj):
        view_context = self.context.get('view')
        if view_context is not None:
            user = view_context.request.user
            if user.is_authenticated() and obj.users.filter(pk=user.pk).exists():
                return True
        return False

    class Meta:
        model = Location
        fields = ('id', 'name', 'slug', 'followed', )


class CountrySerializer(serializers.ModelSerializer):
    """
    A serializer that allows for easier finding of the user's location.
    For the mobile aplication, the native geolocation should prove
    to be more useful, but for order I send it through REST as well.
    """
    capital = serializers.SerializerMethodField('get_capital_location')

    def get_capital_location(self, obj):
        capital = obj.get_capital()
        serializer = LocationListSerializer(capital)
        return serializer.data

    class Meta:
        model = Country
