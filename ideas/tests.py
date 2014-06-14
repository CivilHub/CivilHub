from __future__ import absolute_import
from django.test import TestCase
from .models import Idea


class CategoryTestCase(TestCase):
    def test_valid_category_create(self):
        """ Test if valid category could be created. """
        category = category.objects.create(name='Test', description='Test')
        category.save()
        self.assertEqual(Category.objects.count(), 1)

    def test_invalid_test(self):
        """ Intentionally failed test. """
        self.assertEqual(1, 5)
