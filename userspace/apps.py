from django.apps import AppConfig, apps
from actstream import registry

class UserspaceConfig(AppConfig):
    name = 'userspace'

    def ready(self):
    	registry.register(self.get_model('Badge'))
        registry.register(apps.get_model('auth.user'))
