"""
A forwards compatibility module.

Implements some features of Django 1.4 when the application is run with a lower version of Django:
- text truncating
"""

from __future__ import unicode_literals

from django.utils.functional import allow_lazy
from django.utils.text import truncate_words

class Truncator(object):
    "A simplified version of django.utils.text.Truncator"
    def __init__(self, text):
        self.text = text

    def words(self, num):
        s = truncate_words(self.text, num)
        if s.endswith(' ...'):
            s = s.replace(' ...', '...')
        return s
    words = allow_lazy(words)
