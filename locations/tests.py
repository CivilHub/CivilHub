# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core import cache
from django.contrib.auth.models import User

from ideas.models import Idea

from .models import Location


class MarkerCacheTestCase(TestCase):
    """ """
    fixtures = ['fixtures/users.json',]

    def setUp(self):
        self.cache = cache.get_cache('default')
        self.user = User.objects.first()

    def test_create_and_delete_location(self):
        """ Check that we can create and delete location without errors. """
        location = Location.objects.create(
            creator = self.user,
            name = 'Some Test Place',
            latitude = 30.30,
            longitude = 30.60
        )
        self.assertIsInstance(location, Location)
        self.assertEqual(1, Location.objects.count())
        location.delete()
        self.assertFalse(Location.objects.count())

    def test_update_location_marker_cache(self):
        """
        Check that trying to create location without parent throwing errors.
        """
        location = Location.objects.create(
            creator = self.user,
            name = 'Some Test Place',
            latitude = 30.30,
            longitude = 30.60
        )
        self.assertIsInstance(location, Location)


class DeleteLocationTestCase(TestCase):
    """ Tests for deleting location and moving content to other one. """
    fixtures = ['fixtures/users.json',]

    def setUp(self):
        self.password = 'passphrase'
        self.client = Client()
        self.user = User.objects.create_superuser('tester', 'tester@test.com', self.password)

    def _create_location(self):
        location = Location.objects.create(creator=self.user, name='Test Place')
        return location

    def test_that_content_will_be_moved_to_another_location(self):
        """ When we pass id of another location, content should be moved there. """
        location1 = self._create_location()
        location2 = self._create_location()
        self.assertTrue(self.user.is_superuser)
        # Create some content in first location
        idea = Idea.objects.create(name="test", description="test",
            location=location1, creator=self.user)
        # Check if locations detail page truly exists
        response = self.client.get('/{}/'.format(location1.slug))
        self.assertEqual(response.status_code, 200)
