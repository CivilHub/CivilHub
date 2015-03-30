# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User

from locations.models import Location

from .models import Idea


class IdeaCreateTestCase(TestCase):
    """ Test creating new idea. """
    fixtures = ['fixtures/users.json',]

    def setUp(self):
        self.user = User.objects.first()
        self.location = Location.objects.create(
            name="Sometestplace",
            creator=self.user,
            country_code='PL',
            kind='country'
        )

    def test_create_simple_idea(self):
        """ If this fails, something is REALLY bad. """
        idea = Idea.objects.create(
            name="Some test idea",
            description="This is just for testing",
            creator=self.user,
            location=self.location
        )
        self.assertIsInstance(idea, Idea)

    def test_create_idea_with_unicode_in_title(self):
        """ Test passes, but there is obviously some problem.
        See: https://app.getsentry.com/civilhuborg/civilhub/group/59472529/ """
        idea = Idea.objects.create(
            name="Budowa progu spiętrzającego dla Surferów na rzece Zgłowiączce, Budowa progu spiętrzającego dla Surferów na rzece Zgłowiączce, Budowa progu spiętrzającego dla Surferów na rzece Zgłowiączce",
            description="This is just for testing",
            creator=self.user,
            location=self.location
        )
        self.assertTrue(len(idea.name) <= 64)
        self.assertTrue(len(idea.slug) <= 70)

    def test_that_idea_title_is_sanitized(self):
        """ All tags in title should be removed. """
        idea = Idea.objects.create(
            name='<script src="someevilscript.js"></script>Idea Title',
            description="This is just for testing",
            creator=self.user,
            location=self.location
        )
        self.assertEqual(idea.name, 'Idea Title')
