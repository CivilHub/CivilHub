# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from gallery.image import adjust_uploaded_image, get_image_size

DEFAULT_PATH = settings.DEFAULT_IMG_PATH


def get_image_upload_path(instance, filename):
    """
    Zwraca ścieżkę dla plików obrazów różnych modeli, dodając nazwę modelu.
    """
    model_name = instance.__class__.__name__
    return 'img/{}s/{}.jpg'.format(model_name.lower(), uuid4().hex)


def delete_image_files(base_name, model_name):
    """
    Do tej funkcji przekazujemy nazwę obrazu modelu (bez rozszerzenia i ścieżki)
    oraz nazwę samej klasy modelu w lowercase (np. 'news' lub 'idea'). Funkcja
    usuwa wszystkie obrazy zawierające wspólną nazwę.
    """
    dirname = os.path.join(settings.BASE_DIR, 'media/img', model_name + 's')
    for fname in os.listdir(dirname):
        if base_name in fname:
            try:
                os.unlink(os.path.join(dirname, fname))
            except OSError:
                pass


def remove_image(sender, instance, **kwargs):
    """
    Sygnał wysyłany kiedy usuwamy modele z obrazkami. Django nie usuwa
    ich automatycznie. Należy go zastosować do post_delete.
    """
    if instance.image.name != DEFAULT_PATH:
        delete_image_files(instance.image.name.split('/')[-1].split('.')[0],
            instance.__class__.__name__.lower())


class ImagableItemMixin(models.Model):
    """ Klasa dodająca do modelu pole przechowujące obraz. """
    image = models.ImageField(blank=True, verbose_name=_(u"image"),
        upload_to=get_image_upload_path, default=DEFAULT_PATH)

    class Meta:
        abstract = True

    @property
    def image_height(self):
        """ Zwraca wysokość w pikselach podstawowego obrazu. """
        return get_image_size(self.image.path)[1]

    @property
    def retina_image_height(self):
        """ Jak powyżej, ale zwracamy wysokość obrazka pod retinę. """
        return get_image_size(self.image.path)[1] * 2

    @property
    def image_url(self):
        """ Ponieważ zmieniamy ścieżki, potrzebujemy url obrazka. """
        return "{}_fx.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def retina_image_url(self):
        """ Zwraca ścieżkę do pełnowymiarowego obrazka dla ekranów Retina. """
        return "{}_fx@2x.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def thumbnail(self):
        """ Miniatura do wyświetlenia w widokach list i podsumowaniach. """
        return "{}_thumbnail.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def retina_thumbnail(self):
        """ J/W, z tym, że dla ekranów Retina. """
        return "{}_thumbnail@2x.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def has_image_changed(self):
        """ Metoda sprawdza, czy obrazek dla elementu się zmienił. """
        return self.__initial != self.image

    @property
    def has_default_image(self):
        """ Sprawdza, czy element ma domyślny obraz, czy zmieniony. """
        return self.__initial.name == DEFAULT_PATH

    def save(self, *args, **kwargs):
        # Upewniamy się, że jeżeli wyczyściliśmy pole, przywracamy default
        if not self.image:
            self.image = DEFAULT_PATH
        # Kiedy zmieniamy obrazek, usuwamy stary
        if self.__initial != self.image and self.__initial != DEFAULT_PATH:
            delete_image_files(
                self.__initial.name.split('/')[-1].split('.')[0],
                self.__class__.__name__.lower())
        super(ImagableItemMixin, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(ImagableItemMixin, self).__init__(*args, **kwargs)
        self.__initial = self.image


@python_2_unicode_compatible
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

    def __str__(self):
        return "<Abuse Report from: %s>" % self.sender.get_full_name()
