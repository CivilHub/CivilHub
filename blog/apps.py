from django.apps import AppConfig
from actstream import registry

class BlogStreamConfig(AppConfig):
    name = 'blog'

    def ready(self):
        registry.register(self.get_model('News'))
