from django.apps import AppConfig
from actstream import registry

class LocationStreamConfig(AppConfig):
    name = 'locations'

    def ready(self):
        registry.register(self.get_model('Location'))
