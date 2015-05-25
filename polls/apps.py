from django.apps import AppConfig
from actstream import registry

class PollStreamConfig(AppConfig):
    name = 'polls'

    def ready(self):
        registry.register(self.get_model('Poll'))
