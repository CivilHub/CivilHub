from django.apps import AppConfig
from actstream import registry

class ArticleStreamConfig(AppConfig):
    name = 'articles'

    def ready(self):
        registry.register(self.get_model('Article'))
