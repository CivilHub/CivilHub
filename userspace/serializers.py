# -*- coding: utf-8 -*-
from rest_framework import serializers

from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth
from bookmarks.models import Bookmark


PROVIDERS = ('facebook','google-plus','linkedin','twitter')
GENDERS = ('male','female')


class BookmarkSerializer(serializers.ModelSerializer):
    """ Serializer dla zakładek użytkownika. """
    url = serializers.SerializerMethodField('get_url')
    label = serializers.SerializerMethodField('get_label')

    class Meta:
        model = Bookmark

    def get_url(self, obj):
        return obj.url()

    def get_label(self, obj):
        return obj.__str__()


class SocialAuthenticationDataSerializer(serializers.Serializer):
    """
    Serializuje dane potrzebne podczas logowania/rejestracji użytkownika przez
    jakiekolwiek portale społecznościowe.
    
    Uwaga - ten serializer dzedziczy z podstawowego serializera rest framework,
    jednakże nie jest przeznaczony do podobnych zastosowań i metody, które nie
    zostały tutaj redefiniowane, mogą nie działać zgodnie z oczekiwaniami!!!
    """
    uid = serializers.CharField(max_length=255)
    provider = serializers.ChoiceField(choices=PROVIDERS)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=60, required=False)
    last_name = serializers.CharField(max_length=60, required=False)
    gender = serializers.ChoiceField(choices=GENDERS, required=False)
    birthday = serializers.CharField(max_length=10, required=False)
    url = serializers.URLField(required=False)

    def validate_field(self, label, field, value):
        import re
        if label == 'email':
            if value and not re.match(r'[^@]+@[^@]+\.[^@]+', value):
                self.errors[label] = _("Please provide valid email address")
        if label == 'provider':
            if value and not value in PROVIDERS:
                self.errors[label] = str(value) + _(" is not valid provider choice")
        if label == 'gender':
            if value and not value in GENDERS:
                self.errors[label] = str(value) + _(" is not valid gender choice")
        if label == 'birthday':
            if value and not re.match(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}$', value):
                self.errors[label] = _("Invalid date format (dd/mm/yyyy required)")
        if label == 'url':
            regex = re.compile(
                        r'^(?:http|ftp)s?://' # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                        r'localhost|' #localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?' # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if value and not regex.match(value):
                    self.errors[label] = str(value) + _(" is not valid url")

    def is_valid(self):
        # Szukaj wymaganych pól, które są puste
        for attr, value in self.data.iteritems():
            if self.fields[attr].required and not value:
                self.errors[attr] = _("This field is required")
            else:
                self.validate_field(attr, self.fields[attr], value)
        del self.errors['non_field_errors']
        if self.errors:
            return False
        return True


class SocialAuthSerializer(serializers.ModelSerializer):
    """
    Serializer dla kont social auth w systemie. Umożliwia tworzenie/edycję
    oraz usuwanie kont powiązanych z portalami społecznościowymi.
    """
    class Meta:
        model = UserSocialAuth


class UserAuthSerializer(serializers.ModelSerializer):
    """
    Serializer używany przy autoryzacji użytkowników logujących się przez api
    zewnętrznych dostawców.
    """
    token = serializers.Field(source='auth_token')

    class Meta:
        model = User
        fields = ('id', 'token',)


class UserSerializer(serializers.ModelSerializer):
    """
    Pełny serializer dla użytkownika. W zamierzeniu ma umożliwić tworzenie
    użytkowników przez mobilną aplikację. Definiuje metodę walidowania unikal-
    nych adresów email oraz ustawia hasło nowo utworzonego użytkownika.
    """
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=255, write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User

    def validate(self, attrs):
        if not 'pk' in attrs and 'email' in attrs:
            if User.objects.filter(email=attrs['email']).count():
                self._errors['email'] = _("Provided email address already exists")
        return super(UserSerializer, self).validate(attrs)

    def save_object(self, obj, **kwargs):
        if not obj.pk: obj.set_password(obj.password)
        obj.save(**kwargs)
