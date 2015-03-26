# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy
from social.backends.utils import load_backends, get_backend
from social.pipeline.social_auth import *
from social.pipeline.user import *
from places_core.social_auth import validate_email, \
                                     create_user_profile, \
                                     update_user_social_profile
from .helpers import random_password


class SocialAuthManager(object):
    """
    Fills in Python Social Auth that allows to log in through the mobile
    application. This class is somewhat an additional wrapper for pipeline
    functions that evokes its own methods.
    """
    def __init__(self, provider, uid, data):
        self.strategy = load_strategy()
        self.provider = provider
        self.uid      = uid
        self.data     = data
        self.user     = None
        self.social   = None
        self.is_new   = True
        self.new_assoc= True
        self.username = None
        self.details  = None
        self.is_validated = False
        self.cleaned_data = {}
        self.load_proper_backend()

    def load_proper_backend(self):
        backends = load_backends(settings.AUTHENTICATION_BACKENDS)
        backend_class_name = get_backend(backends, self.provider)
        self.strategy.backend = backend_class_name()

    def verify_(self):
        try:
            self.social = UserSocialAuth.objects.get(provider=self.provider,
                                                      uid=self.uid)
            self.is_new = False
        except UserSocialAuth.DoesNotExist:
            self.social = None

    def social_details_(self):
        self.details = social_details(self.strategy, self.data)['details']

    def validate_email_(self):
        chk = validate_email(self.strategy, self.details, None, self.social)
        if chk and 'user' in chk:
            self.user = chk['user']

    def get_username_(self):
        username = get_username(self.strategy, self.details, self.user)
        self.username = username['username']

    def create_user_(self):
        user = User(
            username = self.username,
            email = self.details['email']
        )
        if 'first_name' in self.data:
            user.first_name = self.data['first_name']
        if 'last_name' in self.data:
            user.last_name = self.data['last_name']
        user.set_password(random_password())
        user.save()
        self.user = user

    def associate_user_(self):
        assoc = associate_user(self.strategy, self.uid, self.user, self.social)
        if assoc:
            self.new_assoc = assoc['new_association']
            self.social = assoc['social']
        else:
            self.new_assoc = True
            self.social = None

    def user_details_(self):
        user_details(self.strategy, self.details, {}, self.user)

    def create_user_profile_(self):
        create_user_profile(self.strategy, self.details, {}, self.user)

    def update_user_social_profile_(self):
        update_user_social_profile(self.strategy, self.details, {}, self.user)

    def is_valid(self):
        if not self.is_validated:
            #self.social_user_()
            self.verify_()
            self.social_details_()
            self.validate_email_()
            self.get_username_()
            if not self.user: self.create_user_()
            self.associate_user_()
            self.create_user_profile_()
            self.update_user_social_profile_()
            self.cleaned_data = {
                'provider': self.provider,
                'uid': self.uid,
                'user': self.user.username if self.user else None,
                'social': self.social.pk if self.social else None,
                'is_new': self.is_new,
                'username': self.username,
            }

    def cleanup_(self):
        user = User.objects.get(username=self.user.username)
        user.delete()
