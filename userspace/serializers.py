# -*- coding: utf-8 -*-
from rest_framework import serializers

from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth
from bookmarks.models import Bookmark

from .models import UserProfile


PROVIDERS = ('facebook','google-plus','linkedin','twitter')
GENDERS = ('male','female')


class BookmarkSerializer(serializers.ModelSerializer):
    """ Serializer for user bookmarks. """
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
    Serializes the data needed when you log in / register as a user by
    any social networking sites.
    
    Note - This serializer inherits rest framework serializer.
    However, it is not intended for similar uses and methods, which do not
    been here redefined, may not work as expected !!!
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
    Serializer auth social accounts in the system. Allows you to create / edit
    and delete accounts that are associated with social networking.
    """
    class Meta:
        model = UserSocialAuth


class UserAuthSerializer(serializers.ModelSerializer):
    """
    Serializer used to authenticate users logging in through the api
    external suppliers.
    """
    token = serializers.Field(source='auth_token')

    class Meta:
        model = User
        fields = ('id', 'token',)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    This serializer is made to be used in list views, presenting detailed info
    about object creator etc.
    """
    url = serializers.Field(source='get_absolute_url')
    thumbnail = serializers.Field(source='thumbnail.url')
    avatar = serializers.Field(source='avatar.url')
    image = serializers.Field(source='image.url')

    class Meta:
        model = UserProfile
        exclude = ('user', 'mod_areas',)


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer presenting user data. Meant to be read-only.
    """
    profile = serializers.SerializerMethodField('get_profile_data')
    full_name = serializers.Field(source='get_full_name')
    organizations = serializers.SerializerMethodField('list_organizations')

    def get_profile_data(self, obj):
        if obj.is_anonymous():
            return None
        serializer = UserProfileSerializer(obj.profile)
        return serializer.data

    def list_organizations(self, obj):
        ngo = {'count': 0, 'items': [], }
        if obj.is_anonymous():
            return ngo
        ngo['count'] = obj.organizations.count()
        for org in obj.organizations.all():
            ngo['items'].append({
                'id': org.pk,
                'name': org.name,
                'url': org.get_absolute_url(), })
        return ngo

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'full_name',
                  'email', 'is_superuser', 'date_joined', 'last_login',
                  'profile', 'organizations', )


class UserSerializer(serializers.ModelSerializer):
    """
    Full serializer for the user. It is intended to help you create
    users through the mobile application. Defines a method of validating a
    unique email addresses and sets the newly created user password.
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
