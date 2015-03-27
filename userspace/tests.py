# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import translation

from .models import LoginData


class APIViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_contents_for_anonymous_user(self):
        response = self.client.get('/api-userspace/contents/')
        self.assertEqual(response.status_code, 404)

    def test_user_actions_for_anonymous_user(self):
        response = self.client.get('/api-userspace/activity/')
        self.assertEqual(response.status_code, 404)


class LoginDataTestCase(TestCase):
    """ Test that Login Data object behaves correctly. """
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_maximum_numbers_of_entries(self):
        """ Check if old login entries will be removed from DB. """
        for i in range(0, 10):
            data = LoginData.objects.create(user=self.user, address='0.0.0.0')
        self.assertEqual(LoginData.objects.filter(user=self.user).count(), 5)


class ProfileCreationTestCase(TestCase):
    """ Test that after user is created, his profile will have proper settings. """
    def test_that_profile_is_really_created(self):
        """ Try to find out user's native language and set it in profile. """
        user = User.objects.create(username='testuser')
        self.assertTrue(user.profile, "We expect user to have profile enabled")
