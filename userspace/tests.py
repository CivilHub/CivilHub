# -*- coding: utf-8 -*-
from django.test import TestCase, Client


class APIViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_contents_for_anonymous_user(self):
        response = self.client.get('/api-userspace/contents/')
        self.assertEqual(response.status_code, 404)

    def test_user_actions_for_anonymous_user(self):
        response = self.client.get('/api-userspace/activity/')
        self.assertEqual(response.status_code, 404)
