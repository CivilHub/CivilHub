# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserSerializerTestCase(TestCase):
    """
    Zestaw testów sprawdzających działanie serializerów dla modelu użytkownika.
    Sprawdzamy tutaj walidację, tworznie nowych obiektów, odczyt i serializację
    istniejących.
    """
    def test_serializer_with_empty_data(self):
        """ Simple test for validate empty requests. """
        serializer = UserSerializer({})
        self.assertFalse(serializer.is_valid())

    def test_serializer_with_basic_data(self):
        """ 
        This test shuld run, as providing this 5 basic fields should create
        new user in database. 
        """
        user_data = {
            'username': 'tester',
            'email': 'notexistingemail@test.pl',
            'first_name': 'Wujek',
            'last_name': 'Fester',
            'password': '123'
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_email_validation(self):
        """
        Check if serializer validates duplicated emails in custom function.
        """
        user_1 = User.objects.create(username='user_1',email='test@test.pl')
        user_1.set_password('passphrase')
        user_1.save()
        user_data = {
            'username': 'tester',
            'email': 'test@test.pl',
            'first_name': 'Wujek',
            'last_name': 'Fester',
            'password': '123'
        }
        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('email' in serializer.errors)


from .managers import SocialAuthManager
from .models import UserProfile
from social.apps.django_app.default.models import UserSocialAuth
from social.strategies.django_strategy import DjangoStrategy
class SocialAuthManagerTestCase(TestCase):
    """
    Testy dla managera social auth pracującego po stronie aplikacji mobilnej.
    """
    def setUp(self):
        self.provider = 'facebook'
        self.uid = '709829435767449'
        self.data = {
            "email": "adrian.kurek13@gmail.com",
            "first_name": "Adrian",
            "last_name": "Kurek",
            "name": "Adrian Kurek",
            "id": "709829435767449",
            "gender": "male",
            "link": "https://www.facebook.com/app_scoped_user_id/709829435767449",
            "locale": "en_us",
            "timezone": 2,
            "updated_time": "2014-07-20T22:09:18+0000",
            "verified": True,
        }
        self.manager = SocialAuthManager(self.provider, self.uid, self.data)

    def test_that_manager_is_valid(self):
        """ Check if manager instance is properly initialized. """
        self.assertTrue(isinstance(self.manager, SocialAuthManager))

    def test_manager_strategy_choice(self):
        """ Check if manager is able to load proper strategy. """
        self.assertTrue(isinstance(self.manager.strategy, DjangoStrategy))

    def test_manager_backend_choice(self):
        """ Check if manager is able to load proper backend. """
        self.assertEquals(self.manager.strategy.backend.name, 'facebook')

    def test_manager_can_harvest_data(self):
        """ Check if manager is able to get data from social account. """
        manager_data = self.manager.is_valid()
        self.assertEqual(self.manager.details['fullname'], 'Adrian Kurek')

    def test_manager_can_get_username(self):
        """ Check if manager can obtain user's username. """
        manager_data = self.manager.is_valid()
        self.assertIsNotNone(self.manager.username)

    def test_manager_associate_users(self):
        """ Check if manager is able to associate user and social user. """
        manager_data = self.manager.is_valid()
        self.assertTrue(self.manager.new_assoc)
        self.assertIsNotNone(self.manager.user)
        self.assertIsNotNone(self.manager.social)
        self.assertTrue(isinstance(self.manager.social, UserSocialAuth))

    def test_manager_creates_user_profile(self):
        """ Check if user profile is created along with new user. """
        manager_data = self.manager.is_valid()
        self.assertIsNotNone(self.manager.user.profile)
        self.assertTrue(isinstance(self.manager.user.profile, UserProfile))
