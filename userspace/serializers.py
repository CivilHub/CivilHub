# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from bookmarks.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer dla zakładek użytkownika.
    """
    key = serializers.CharField(max_length=16, required=False)
    
    class Meta:
        model = Bookmark