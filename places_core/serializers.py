# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType


class ContentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer umożliwiający pobieranie id typu zawartości na podstawie nazwy
    aplikacji/modelu i vice-versa. Przydatne kiedy chcemy ustalić typ zawartości
    dla modeli relacyjnych (komentarze, zakładki itp.).
    """
    class Meta:
        model = ContentType