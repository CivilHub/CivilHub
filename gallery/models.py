# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from locations.models import Location
from .image import crop, crop_gallery_thumb, delete_cropped_thumb, fix_path
from .managers import ContentGalleryManager
from .signals import adjust_images, cleanup_gallery, cleanup_image
from .storage import check, upload_path


@python_2_unicode_compatible
class GalleryItem(models.Model):
    """
    Basic abstract model for gallery items. All types of gallery items should
    inherit it.
    """

    class Meta:
        abstract = True

    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, blank=True, null=True)
    picture_name = models.CharField(max_length=255, blank=True, default=u'')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def get_filepath(self):
        """
        This method returns full pathname to item gallery. It may be useful for
        other custom views.
        """
        return str(settings.MEDIA_ROOT)

    def get_filename(self):
        """ Returns full file path and filename.
        """
        path = self.get_filepath()
        return os.path.join(path, self.picture_name)

    def save(self, *args, **kwargs):
        if self.description:
            self.description = strip_tags(self.description)
        super(GalleryItem, self).save(*args, **kwargs)

    def delete(self):
        filename = self.picture_name
        filepath = self.get_filepath()
        thumbs = os.path.join(filepath, 'thumbs')
        for s in settings.THUMB_SIZES:
            f = os.path.join(thumbs,
                             str(s[0]) + 'x' + str(s[1]) + '_' + filename)
            try:
                os.unlink(f)
            except Exception:
                pass
        try:
            os.unlink(self.get_filename())
        except Exception:
            pass
        super(GalleryItem, self).delete()

    def __str__(self):
        return self.picture_name


class UserGalleryItem(GalleryItem):
    """ This simple gallery item class handles user media.
    """

    def url(self):
        """
        Returns picture url. This function is most useful for views.
        """
        return settings.MEDIA_URL + self.user.username + '/' + self.picture_name

    def get_thumbnail(self, size):
        """
        This function returns url to thumbnail of photo. Size parameter is man-
        datory and related to thumb sizes declared in views module. It should
        be touple or list containing images width and height.
        """
        thumbname = str(size[0]) + 'x' + str(size[1]) + '_' + self.picture_name
        return settings.MEDIA_URL + self.user.username + '/thumbs/' + thumbname

    def get_filepath(self):
        return str(os.path.join(settings.MEDIA_ROOT, str(self.user.username)))

    def thumb_small(self):
        return self.get_thumbnail((128, 128))

    def thumb_big(self):
        return self.get_thumbnail((256, 256))

    def thumb_cropped(self):
        return settings.MEDIA_URL + self.user.username + '/cropped_' + self.picture_name


models.signals.post_save.connect(crop_gallery_thumb, sender=UserGalleryItem)
models.signals.post_delete.connect(delete_cropped_thumb,
                                   sender=UserGalleryItem)


class LocationGalleryItem(GalleryItem):
    """
    This is basic class for items in location's gallery. File upload is handled
    other way, here we just add some additional data for our pictures, like
    comment and name.
    """
    location = models.ForeignKey(Location, related_name='pictures')

    def url(self):
        """ Returns picture url. This function is most useful for views.
        """
        return settings.MEDIA_URL + self.location.slug + '/' + self.picture_name

    def get_thumbnail(self, size):
        """
        This function returns url to thumbnail of photo. Size parameter is man-
        datory and related to thumb sizes declared in views module. It should
        be touple or list containing images width and height.
        """
        thumbname = str(size[0]) + 'x' + str(size[1]) + '_' + self.picture_name
        return settings.MEDIA_URL + self.location.slug + '/thumbs/' + thumbname

    def thumb_cropped(self):
        return settings.MEDIA_URL + self.location.slug + '/cropped_' + self.picture_name

    def get_filepath(self):
        return str(os.path.join(settings.MEDIA_ROOT, self.location.slug))

    def get_absolute_url(self):
        return reverse('locations:picture',
                       kwargs={'slug': self.location.slug,
                               'pk': self.pk, })

    def __str__(self):
        return self.name or self.picture_name


models.signals.post_save.connect(crop_gallery_thumb,
                                 sender=LocationGalleryItem)
models.signals.post_delete.connect(delete_cropped_thumb,
                                   sender=LocationGalleryItem)


@python_2_unicode_compatible
class ContentObjectGallery(models.Model):
    """
    This model allows us to create galleries related to any other model.
    This way we can manage galleries e.g. for projects. The `published_id`
    field may be empty, which means that we have stand-alone gallery.
    """
    name = models.CharField(max_length=64,
                            blank=True,
                            default="",
                            verbose_name=_(u"name"))
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    published_in = generic.GenericForeignKey('content_type', 'object_id')
    dirname = models.CharField(max_length=64, blank=True)

    objects = ContentGalleryManager()

    @property
    def cover(self):
        if self.pictures.count():
            return self.pictures.first().thumb
        return None

    def save(self, *args, **kwargs):
        check(self)
        super(ContentObjectGallery, self).save(*args, **kwargs)

    def get_absolute_url(self):
        url_entry = 'gallery:album-preview'
        url_kwarg = {'pk': self.pk, }
        if self.published_in is not None:
            model_name = self.published_in._meta.model_name
            if model_name == 'socialproject':
                url_entry = 'projects:gallery-preview'
                url_kwarg = {
                    'slug': self.published_in.slug,
                    'gallery_pk': self.pk,
                }
            elif model_name == 'idea':
                url_entry = 'locations:idea_detail'
                url_kwarg = {
                    'place_slug': self.published_in.location.slug,
                    'slug': self.published_in.slug,
                }
        return reverse(url_entry, kwargs=url_kwarg)

    def __str__(self):
        if len(self.name):
            return self.name
        elif self.published_in is not None:
            return u"Image Gallery for %s" % self.published_in.__unicode__()
        else:
            return u"Unpublished Image Gallery"

    class Meta:
        verbose_name = _(u"image gallery")
        verbose_name_plural = _(u"image galleries")


models.signals.post_delete.connect(cleanup_gallery,
                                   sender=ContentObjectGallery)


@python_2_unicode_compatible
class ContentObjectPicture(models.Model):
    """
    Picture have to belong to exactly one gallery. For now it's better to avoid
    editing of 'gallery' and 'image' fields, because files will stay in wrong
    directories and may become unavailable.
    """
    name = models.CharField(max_length=64,
                            default="",
                            blank=True,
                            verbose_name=_(u"name"))
    description = models.TextField(blank=True,
                                   default="",
                                   verbose_name=_(u"description"))
    gallery = models.ForeignKey(ContentObjectGallery,
                                related_name="pictures",
                                verbose_name=_(u"gallery"))
    image = models.ImageField(verbose_name=_(u"image"), upload_to=upload_path)
    date_uploaded = models.DateTimeField(auto_now_add=True,
                                         verbose_name=_(u"date uploaded"))
    uploaded_by = models.ForeignKey(User, verbose_name=_(u"uploaded by"))

    @property
    def thumb(self):
        return fix_path(self.image.url)

    @property
    def thumb_small(self):
        return fix_path(self.image.url, 'SMALL')

    def get_absolute_url(self):
        url_entry = 'gallery:picture-detail'
        url_kwarg = {'pk': self.pk, }
        publisher = self.gallery.published_in
        if publisher is not None:
            model_name = publisher._meta.model_name
            if model_name == 'socialproject':
                url_entry = 'projects:picture-detail'
                url_kwarg = {'slug': publisher.slug, 'picture_pk': self.pk, }
            elif model_name == 'idea':
                url_entry = 'locations:idea_detail'
                url_kwarg = {
                    'place_slug': publisher.location.slug,
                    'slug': publisher.slug,
                }
        return reverse(url_entry, kwargs=url_kwarg)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_uploaded', ]
        verbose_name = _(u"picture")
        verbose_name_plural = _(u"pictures")


models.signals.post_save.connect(adjust_images, sender=ContentObjectPicture)
models.signals.post_delete.connect(cleanup_image, sender=ContentObjectPicture)
