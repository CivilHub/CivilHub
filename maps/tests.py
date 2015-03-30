# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import cache
from django.contrib.auth.models import User

from locations.models import Location

from .models import MapPointer
from .helpers import make_region_cluster

# Watch out! The tests here use default cache settings,
# so better not run them on production until it's fixed.

class MarkerCacheTestCase(TestCase):
    """ Test that marker are correctly created and deleted for different content types. """
    fixtures = ['fixtures/users.json',
                'fixtures/locations.json',]

    def setUp(self):
        self.cache = cache.get_cache('default')
        self.user = User.objects.first()
        self.main_locations = Location.objects.filter(kind__in=['PPLC', 'PPLA',])

    def _create_location(self):
        """ Helper that just creates new dummy location. """
        location = Location.objects.create(
            name="New Reno",
            creator=self.user,
            latitude=123.12,
            longitude=-24.3,
            country_code='US'
        )
        return location

    def test_that_marker_is_created_for_new_location(self):
        """ Check if new marker is created when location is saved. """
        location = self._create_location()
        self.assertEqual(len(MapPointer.objects.for_location(location)), 1)

    def test_that_marker_is_deleted_along_with_location(self):
        """ Check if marker is deleted when location is deleted. """
        location = self._create_location()
        location.delete()
        self.assertFalse(len(MapPointer.objects.for_location(location)))

    def test_that_marker_clusters_are_updated(self):
        """ Test function that creates and updates map marker clusters. """
        for location in self.main_locations:
            make_region_cluster(location)
            self.assertNotEqual(self.cache.get(str(location.pk) + '_childlist'), None)

    def tearDown(self):
        self.cache.delete('allcountries')
        for location in self.main_locations:
            self.cache.delete(str(location.pk) + '_childlist')
