from django.apps import AppConfig
from actstream import registry

class GuideStreamConfig(AppConfig):
    name = 'guides'

    def ready(self):
        registry.register(self.get_model('Guide'))
