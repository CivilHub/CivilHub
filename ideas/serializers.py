# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import Category, Idea, Vote


class IdeaVoteSerializer(serializers.ModelSerializer):
    """
    Prosty serializer dla obiektów powiązanych z głosami na idee.
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