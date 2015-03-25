# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest.serializers import TranslatedModelSerializer

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
