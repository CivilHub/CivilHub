from django.apps import AppConfig
from actstream import registry

class IdeaStreamConfig(AppConfig):
    name = 'ideas'

    def ready(self):
        registry.register(self.get_model('Idea'))
        registry.register(self.get_model('Vote'))
