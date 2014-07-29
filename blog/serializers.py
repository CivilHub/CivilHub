# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import News


class NewsSimpleSerializer(serializers.ModelSerializer):
    """
    Simplified News object serializer for mobile API.
    """
    id = serializers.Field(source='pk')
    slug = serializers.SlugField(required=False)
    
    class Meta:
        model = News
        exclude = ('creator',)