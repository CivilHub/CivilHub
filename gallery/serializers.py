# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import UserGalleryItem


class UserMediaSerializer(serializers.ModelSerializer):
    """ Serializer for items in user gallery. """
    id = serializers.Field(source='pk')
    picture_name = serializers.CharField(required=False)
    picture_url = serializers.SerializerMethodField('get_url')
    thumbnail = serializers.SerializerMethodField('get_thumbnail')

    def get_url(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.build_absolute_uri(obj.url())
        return obj.url()

    def get_thumbnail(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.build_absolute_uri(obj.get_thumbnail((128,128)))
        return obj.get_thumbnail((128.128))

    def pre_save(self, obj):
        request = self.context.get('request', None)
        self.user = request.user

    class Meta:
        model = UserGalleryItem
        fields = ('id', 'picture_name', 'picture_url', 'thumbnail')
