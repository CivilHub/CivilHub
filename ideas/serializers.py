# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import Category, Idea


class IdeaSimpleSerializer(serializers.ModelSerializer):
    """
    Simple idea objects serializer for mobile API.
    """
    id = serializers.Field(source='pk')
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Idea
        exclude = ('creator',)