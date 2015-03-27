# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import cache
from django.contrib.auth.models import User

from locations.models import Location


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
