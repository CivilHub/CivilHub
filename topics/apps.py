from django.apps import AppConfig
from actstream import registry

class DiscussionStreamConfig(AppConfig):
    name = 'topics'

    def ready(self):
        registry.register(self.get_model('Discussion'))
        registry.register(self.get_model('Entry'))
