# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer to show short info during mouse hover
    """
    class Meta:
        model = User
        fields = ('username', 'email')
