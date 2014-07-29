# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import Category, Discussion, Entry


class ForumCategorySimpleSerializer(serializers.ModelSerializer):
    """
    Serializers data for forum categories in simple version made for 
    mobile app to present list of categories and create some way to 
    manage them.
    """
    class Meta:
        model = Category


class ForumTopicSimpleSerializer(serializers.ModelSerializer):
    """
    Simple serializer for mobile application. Serializes data for
    entire discussion object.
    """
    id = serializers.Field(source='pk')
    slug = serializers.SlugField(required=False)
    
    class Meta:
        model = Discussion
        exclude = ('creator',)


class ForumEntrySimpleSerializer(serializers.ModelSerializer):
    """
    This is serializer for single forum entry (response).
    """
    class Meta:
        model = Entry