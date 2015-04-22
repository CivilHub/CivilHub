from django.apps import AppConfig
from actstream import registry


class NGOStreamConfig(AppConfig):
    name = 'organizations'

    def ready(self):
        registry.register(self.get_model('Organization'))
