# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.core import cache
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

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


class MapPointerViewTestCase(TestCase):
    """ Test responses for requests to map view when specific location is selected.
    see: https://app.getsentry.com/civilhuborg/civilhub/group/60399009/ """
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(username='tester')
        cls.client = Client()

    def test_map_response_for_location_with_geo_params(self):
        """ Test that everything is fine when location has some map pointers. """
        location = Location.objects.create(
            name="Testowice",
            creator=self.user,
            latitude=-19.90,
            longitude=66.66)
        response = self.client.get('/maps/info/{}/{}/'.format(
            ContentType.objects.get_for_model(Location).pk, location.pk))
        self.assertEqual(response.status_code, 200)

    def test_map_response_for_location_without_map_marker(self):
        """ This is test for 500 error showing up when location has no
        related map markers. """
        location = Location.objects.create(
            name="Testowice",
            creator=self.user)
        response = self.client.get('/maps/info/{}/{}/'.format(
            ContentType.objects.get_for_model(Location).pk, location.pk))
        self.assertEqual(response.status_code, 404)
