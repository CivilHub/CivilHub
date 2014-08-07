# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from bookmarks.models import Bookmark


class UserAuthSerializer(serializers.ModelSerializer):
    """
    Serializer używany przy autoryzacji użytkowników logujących się przez api
    zewnętrznych dostawców.
    """
    token = serializers.Field(source='auth_token')

    class Meta:
        model = User
        fields = ('id', 'token',)


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer dla zakładek użytkownika.
    """
    key = serializers.CharField(max_length=16, required=False)
    
    class Meta:
        model = Bookmark


class UserSerializer(serializers.ModelSerializer):
    """
    Pełny serializer dla użytkownika. W zamierzeniu ma umożliwić tworzenie
    użytkowników przez mobilną aplikację. Definiuje metodę walidowania unikal-
    nych adresów email oraz ustawia hasło nowo utworzonego użytkownika.
    """
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = User

    def validate(self, attrs):
        if not 'pk' in attrs and 'email' in attrs:
            if User.objects.filter(email=attrs['email']).count():
                self._errors['email'] = _("Provided email address already exists")
        return super(UserSerializer, self).validate(attrs)

    def save_object(self, obj, **kwargs):
        obj.set_password(obj.password)
        obj.save(**kwargs)
