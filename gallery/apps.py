from django.apps import AppConfig
from actstream import registry

class GalleryStreamConfig(AppConfig):
    name = 'gallery'

    def ready(self):
        registry.register(self.get_model('LocationGalleryItem'))
        registry.register(self.get_model('ContentObjectGallery'))
        registry.register(self.get_model('ContentObjectPicture'))
