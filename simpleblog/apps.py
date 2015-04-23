from django.apps import AppConfig
from actstream import registry


class SimpleBlogStreamConfig(AppConfig):
    name = 'simpleblog'

    def ready(self):
        registry.register(self.get_model('BlogEntry'))
