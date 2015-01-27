# -*- coding: utf-8 -*-
import os
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.contrib.comments.models import BaseCommentAbstractModel
from django.contrib.auth.models import User

DEFAULT_IMG_PATH = "img/item.jpg"


def get_image_upload_path(instance, filename):
    """
    Zwraca ścieżkę dla plików obrazów różnych modeli, dodając nazwę modelu.
    """
    model_name = instance.__class__.__name__
    return 'img/{}s/{}{}'.format(model_name.lower(),
        uuid4().hex, os.path.splitext(filename)[1])


def remove_image(sender, instance, **kwargs):
    """
    Sygnał wysyłany kiedy usuwamy modele z obrazkami. Django nie usuwa
    ich automatycznie. Należy go zastosować do post_delete.
    """
    if instance.image.name != DEFAULT_IMG_PATH:
        try:
            os.unlink(instance.image.path)
        except OSError, IOError:
            pass


class ImagableItemMixin(models.Model):
    """ Klasa dodająca do modelu pole przechowujące obraz. """
    image = models.ImageField(blank=True,
        upload_to=get_image_upload_path, default=DEFAULT_IMG_PATH)

    def image_url(self):
        """ Ponieważ zmieniamy ścieżki, potrzebujemy url obrazka. """
        if self.image.name == DEFAULT_IMG_PATH:
            img_url = DEFAULT_IMG_PATH
        else:
            img_url = get_image_upload_path(self, self.image.path)
        return settings.MEDIA_URL + img_url


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
