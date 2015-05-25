# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core import cache
from django.contrib.auth.models import User

from actstream.actions import follow

from ideas.models import Idea

from .models import Location
from .forms import LocationForm
from .helpers import get_followers_from_location


class ParentChildrenChainTestCase(TestCase):
    """ """
    fixtures = ['fixtures/users.json',
                'fixtures/locations.json',]

    def test_location_parent_id_list(self):
        l = Location.objects.get(slug='brzeg-pl-1')
        ids = l.get_parent_id_list()
        self.assertEqual(len(ids), 2)
        self.assertIn(l.parent.pk, ids)
        self.assertIn(l.parent.parent.pk, ids)
        pl = Location.objects.get(ids[-1])
        self.assertEqual(pl.country_code, 'PL')
        self.assertEqual(pl.kind, 'country')


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


class GetFollowersHelperTestCase(TestCase):
    """ This is test case for helper getting followers from selected location.
        Just remember that in this test case we also have superuser enabled and
        he is following our country location, that's why there is always one
        more follower in returned list.
    """
    fixtures = ['fixtures/users.json',
                'fixtures/countries.json',
                'fixtures/locations.json',]

    def setUp(self):
        self.user1 = User.objects.create(username='testuser1', email="test1@civilhub.org")
        self.user2 = User.objects.create(username='testuser2', email="test2@civilhub.org")
        self.user3 = User.objects.create(username='testuser3', email="test3@civilhub.org")
        self.country = Location.objects.get(slug='poland-pl')
        self.region = self.country.location_set.first()
        self.city = self.region.location_set.first()
        follow(self.user1, self.country)
        self.country.users.add(self.user1)
        follow(self.user2, self.region)
        self.region.users.add(self.user2)
        follow(self.user3, self.city)
        self.city.users.add(self.user3)

    def test_getting_followers_without_deep_option(self):
        """ Without deep option enabled function should return only this location's followers. """
        followers = get_followers_from_location(self.country.pk)
        self.assertEqual(len(followers), 2)
        self.assertIn(self.user1, followers)
        self.assertNotIn(self.user2, followers)
        self.assertNotIn(self.user3, followers)

    def test_getting_followers_with_deep_from_country(self):
        """ Function should return all followers from country and children locations. """
        followers = get_followers_from_location(self.country.pk, deep=True)
        self.assertEqual(len(followers), 4)
        self.assertIn(self.user1, followers)
        self.assertIn(self.user2, followers)
        self.assertIn(self.user3, followers)

    def test_getting_followers_with_deep_from_region(self):
        """ This time we shoud see just followers for region and city. """
        followers = get_followers_from_location(self.region.pk, deep=True)
        self.assertEqual(len(followers), 3)
        self.assertNotIn(self.user1, followers)
        self.assertIn(self.user2, followers)
        self.assertIn(self.user3, followers)

    def test_getting_followers_with_deep_from_city(self):
        """
        This location children have no followers, so we should
        see only user3 and superuser on list.
        """
        followers = get_followers_from_location(self.city.pk, deep=True)
        self.assertEqual(len(followers), 2)
        self.assertNotIn(self.user1, followers)
        self.assertNotIn(self.user2, followers)
        self.assertIn(self.user3, followers)
