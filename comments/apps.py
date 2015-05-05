from django.apps import AppConfig
from actstream import registry

class CommentStreamConfig(AppConfig):
    name = 'comments'

    def ready(self):
        registry.register(self.get_model('CustomComment'))
        registry.register(self.get_model('CommentVote'))
