# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest.serializers import TranslatedModelSerializer
from .models import Category, Idea, Vote


class IdeaCategorySerializer(TranslatedModelSerializer):
    """ """
    class Meta:
        model = Category


class IdeaVoteSerializer(serializers.ModelSerializer):
    """
    A simple serializer for object connected with votes in ideas.
    """
    class Meta:
        model = Vote

    def validate(self, attrs):
        """ Metoda sprawdza, czy użytkownik głosował już na ten pomysł. """
        if Vote.objects.filter(user=attrs['user'],idea=attrs['idea']).count():
            self._errors['non_field_errors'] = _("You voted already for this idea")
        return super(IdeaVoteSerializer, self).validate(attrs)


class IdeaSimpleSerializer(serializers.ModelSerializer):
    """
    Simple idea objects serializer for mobile API.
    """
    id = serializers.Field(source='pk')
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Idea
        exclude = ('creator',)