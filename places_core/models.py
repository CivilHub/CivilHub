# -*- coding: utf-8 -*-
import os
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User

from gallery.image import adjust_uploaded_image

DEFAULT_PATH = settings.DEFAULT_IMG_PATH


def get_image_upload_path(instance, filename):
    """
    Zwraca ścieżkę dla plików obrazów różnych modeli, dodając nazwę modelu.
    """
    model_name = instance.__class__.__name__
    return 'img/{}s/{}.jpg'.format(model_name.lower(), uuid4().hex)


def remove_image(sender, instance, **kwargs):
    """
    Sygnał wysyłany kiedy usuwamy modele z obrazkami. Django nie usuwa
    ich automatycznie. Należy go zastosować do post_delete.
    """
    if instance.image.name != DEFAULT_PATH:
        try:
            os.unlink(instance.image.path)
        except Exception:
            pass


def adjust_images(sender, instance, **kwargs):
    if instance.image.name == DEFAULT_PATH:
        return True
    adjust_uploaded_image(instance.image.path)


class ImagableItemMixin(models.Model):
    """ Klasa dodająca do modelu pole przechowujące obraz. """
    image = models.ImageField(blank=True,
        upload_to=get_image_upload_path, default=DEFAULT_PATH)

    @property
    def image_url(self):
        """ Ponieważ zmieniamy ścieżki, potrzebujemy url obrazka. """
        return settings.MEDIA_URL + self.image.name

    @property
    def has_image_changed(self):
        """ Metoda sprawdza, czy obrazek dla elementu się zmienił. """
        return self.__initial != self.image

    def __init__(self, *args, **kwargs):
        super(ImagableItemMixin, self).__init__(*args, **kwargs)
        self.__initial = self.image

    def save(self, *args, **kwargs):
        """ Upewniamy się, że jeżeli zmieniamy obrazek, usuniemy stary. """
        if self.__initial.name != DEFAULT_PATH:
            if self.has_image_changed:
                try:
                    os.unlink(self.__initial.path)
                except Exception:
                    pass
        super(ImagableItemMixin, self).save(*args, **kwargs)


class AbuseReport(BaseCommentAbstractModel):
    """
    Abuse reports to show to admins and moderators. All registered users
    can send reports, but no one except superadmins is allowed to delete
    and edit them.
    """
    sender  = models.ForeignKey(User)
    comment = models.CharField(max_length=2048)
    status  = models.BooleanField(default=False)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
