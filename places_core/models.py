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
    Return a path of files, images of different models and adds the model name.
    """
    model_name = instance.__class__.__name__
    return 'img/{}s/{}.jpg'.format(model_name.lower(), uuid4().hex)


def delete_image_files(base_name, model_name):
    """
    To this function we pass the model image's name (without the extension
    and without the path) and the name of the model class itself in lowercase
    (e.g. 'news' or 'idea'). This function deletes all images that contain a
    common name.
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
    A signal that is sent when we delete models with images. Django
    does not delete them automatically. It should be used in post_delete.
    """
    if instance.image.name != DEFAULT_PATH:
        delete_image_files(instance.image.name.split('/')[-1].split('.')[0],
            instance.__class__.__name__.lower())


class ImagableItemMixin(models.Model):
    """ A class that adds a field to the model that stores the image."""
    image = models.ImageField(blank=True, verbose_name=_(u"image"),
        upload_to=get_image_upload_path, default=DEFAULT_PATH)

    class Meta:
        abstract = True

    @property
    def image_height(self):
        """ Returns the height in pixels of the base image."""
        return get_image_size(self.image.path)[1]

    @property
    def retina_image_height(self):
        """ Same as above but the height is return for retina. """
        return get_image_size(self.image.path)[1] * 2

    @property
    def image_url(self):
        """ Because we change paths, we need the url of the image. """
        return "{}_fx.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def retina_image_url(self):
        """ Returns the path to a full-scale image for Retina screen. """
        return "{}_fx@2x.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def thumbnail(self):
        """ A minature to be displayed in list view and summary."""
        return "{}_thumbnail.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def retina_thumbnail(self):
        """ Same as above but for Retina. """
        return "{}_thumbnail@2x.jpg".format(os.path.splitext(self.image.url)[0])

    @property
    def has_image_changed(self):
        """ This method checks whether the image for the element was changed."""
        return self.__initial != self.image

    @property
    def has_default_image(self):
        """ Checks whether the element has a default image or whether it was changed. """
        return self.__initial.name == DEFAULT_PATH

    def save(self, *args, **kwargs):
        # We make sure that if we clear the field, the default will be brought back
        if not self.image:
            self.image = DEFAULT_PATH
        # When we change the image, we delete the old one
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
    REASONS = (
        (1, _(u"Pornography")),
        (2, _(u"Violence/indicent content")),
        (3, _(u"Insults/spread of hatred")),
        (4, _(u"Dangerious activities")),
        (5, _(u"Usage of children")),
        (6, _(u"Spam or other misleading content")),
        (7, _(u"Violence of my copyrights")),
        (8, _(u"Violence of my privacy")),
        (9, _(u"Other legal claims")),
        (10, _(u"Duplicate")),
        (11, _(u"False information")),
        (12, _(u"Is not suitable")),
    )

    sender  = models.ForeignKey(User)
    comment = models.CharField(max_length=2048, default="", blank=True,
                               verbose_name=_(u"comment"))
    status  = models.BooleanField(default=False)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    reason = models.PositiveIntegerField(choices=REASONS, default=12,
                                         verbose_name=_(u"reason"))

    def __str__(self):
        return "<Abuse Report from: %s>" % self.sender.get_full_name()


class SearchTermRecordManager(models.Manager):
    """
    """
    def count_most_popular(self):
        terms = {}
        for record in self.all():
            if record.term not in terms:
                terms[record.term] = len(self.filter(term=record.term))
            else:
                continue
        return sorted(terms.items(), key=lambda x: x[1], reverse=True)


@python_2_unicode_compatible
class SearchTermRecord(models.Model):
    """ This model records search term when user filled search form.
    """
    term = models.CharField(max_length=255, verbose_name=_(u"search term"))
    ip_address = models.IPAddressField(blank=True, null=True, verbose_name=_(u"ip address"))
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_(u"user"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date"))
    content_types = models.CharField(max_length=255, default="", blank=True, verbose_name=(u"content types"))

    objects = SearchTermRecordManager()

    def __str__(self):
        return _(u"Search for") + " '%s'" % self.term

    class Meta:
        ordering = ['-date_created', ]
        verbose_name = _(u"search record")
        verbose_name_plural = _(u"search records")
