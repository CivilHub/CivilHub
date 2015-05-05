"""
Default application configuration.
In use as of Django 1.7.
"""
from django.apps import AppConfig


class PostmanConfig(AppConfig):
    name = 'postman'

    def ready(self):
        from .models import setup
        setup()