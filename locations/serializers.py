# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import Location


class SimpleLocationSerializer(serializers.ModelSerializer):
    """
    Simple location serializer for mobile API. Allows to list, add and manage
    location objects in database. Provides standard CRUD operations set.
    """
    class Meta:
        model = Location