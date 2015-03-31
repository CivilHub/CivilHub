# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core import cache
from django.contrib.auth.models import User

from ideas.models import Idea

from .models import Location
from .forms import LocationForm


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
    """
    Tests for deleting location and moving content to other one.
    TODO: this is just dummy test for now.
    """
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


class CreateLocationFormTestCase(TestCase):
    """ Test form for creating new location. """
    fixtures = ['fixtures/users.json',
                'fixtures/countries.json',
                'fixtures/locations.json',]

    def test_location_form_with_valid_data(self):
        """ Test that form with valid data works and location is saved properly. """
        data = {
            'name': 'Testowice',
            'latitude': 30.00,
            'longitude': -120.15,
            'parent': Location.objects.get(slug='warsaw-pl').pk,
            'population': 100,
            'kind': 'PPLA',
        }
        form = LocationForm(data)
        self.assertTrue(form.is_valid())
        form.instance.creator = User.objects.first()
        location = form.save()
        self.assertIsInstance(location, Location)
        self.assertEqual(location.country_code, location.parent.country_code)
        self.assertEqual(location.mappointer_set.count(), 1)
        mp = location.mappointer_set.first()
        self.assertEqual(mp.latitude, location.latitude)
        self.assertEqual(mp.longitude, location.longitude)

    def test_location_form_without_parent(self):
        """ Test that users are allowed to create locations only inside some
        parent location, at least they have to choose country and region. """
        data = {
            'name': 'Testowice',
            'latitude': 30.00,
            'longitude': -120.15,
            'population': 100,
            'kind': 'PPLA',
        }
        form = LocationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('parent', form.errors)

    def test_location_form_with_country_as_parent(self):
        """ Users should not be able to create locations that are direct country
        location children. They have to choose at least some region. """
        data = {
            'name': 'Testowice',
            'latitude': 30.00,
            'longitude': -120.15,
            'population': 100,
            'kind': 'PPLA',
            'parent': Location.objects.get(slug='poland-pl').pk,
        }
        form = LocationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('parent', form.errors)
