from django.apps import AppConfig
from actstream import registry

class ProjectStreamConfig(AppConfig):
    name = 'projects'

    def ready(self):
        registry.register(self.get_model('SocialProject'))
        registry.register(self.get_model('TaskGroup'))
        registry.register(self.get_model('Task'))
        registry.register(self.get_model('SocialForumTopic'))
        registry.register(self.get_model('SocialForumEntry'))
