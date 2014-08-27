# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import Country


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializer umożliwiający łatwiejsze namierzanie lokalizacji użytkownika.
    Dla aplikacji mobilnej raczej bardziej przydatne będą natywne funkcje
    geolokacji, ale dla porządku to też puszczam przez REST.
    """
    class Meta:
        model = Country


class CountryCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=2)
    name = serializers.Field(source='location.name')

    class Meta:
        model = Country
        fields = ('code', 'name',)
