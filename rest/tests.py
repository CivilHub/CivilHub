# -*- coding: utf-8 -*-
from django.test import TestCase
from .serializers import TranslatedModelSerializer


class TranslatedModelSerializerTestCase(TestCase):
    """
    """
    def setUp(self):
        pass

    def test_if_serializer_is_properly_invoked(self):
        serializer = TranslatedModelSerializer({})
        self.assertFalse(serializer.is_valid())
