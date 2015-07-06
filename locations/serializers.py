# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

from actstream.models import following
from rest_framework import serializers
from rest_framework.pagination import PaginationSerializer

from .models import Location, Country


class LocationMapDataSerializer(serializers.ModelSerializer):
    """ Serializer for map inputs - determine initial position and zoom.
    """
    name = serializers.Field(source='__unicode__')
    lat = serializers.SerializerMethodField('get_lat')
    lng = serializers.SerializerMethodField('get_lng')
    zoom = serializers.SerializerMethodField('get_zoom')

    def get_lat(self, obj):
        try:
            return self._get_lat_lng(obj, 'latitude')
        except AttributeError:
            return 0.0

    def get_lng(self, obj):
        try:
            return self._get_lat_lng(obj, 'longitude')
        except AttributeError:
            return 0.0

    def get_zoom(self, obj):
        if obj.kind == 'country':
            return 4
        elif obj.kind == 'region':
            return 7
        return 12

    def _get_lat_lng(self, obj, attr):
        if obj.kind == 'country' or obj.kind == 'region':
            retval = getattr(obj.get_capital, attr)
        else:
            retval = getattr(obj, attr)
        if retval is None:
            return 0.0
        return float(retval)

    class Meta:
        model = Location
        fields = ('id', 'name', 'lat', 'lng', 'zoom', 'kind', )


class AutocompleteLocationSerializer(serializers.ModelSerializer):
    """ This is serializer especially for autocomplete.
    """
    value = serializers.Field(source='pk')
    label = serializers.SerializerMethodField('get_label')
    following = serializers.SerializerMethodField('check_followed')
    template = serializers.SerializerMethodField('get_template')

    def get_label(self, obj):
        names = [obj.__unicode__(), ]
        qs = Location.objects.filter(pk__in=obj.get_parents)\
                            .order_by('-kind').values('name', )
        names = names + [x['name'] for x in qs]
        return " ".join(names)

    def check_followed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        if request.user.is_anonymous():
            return False
        return obj in following(request.user)

    def get_template(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous():
            return 'simple'
        return 'normal'

    class Meta:
        model = Location
        fields = ('value', 'label', 'following', 'template', )


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
