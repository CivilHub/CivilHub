# -*- coding: utf-8 -*-
import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from locations.models import Location
from .image import crop_gallery_thumb, delete_cropped_thumb


class GalleryItem(models.Model):
    """
    Basic abstract model for gallery items. All types of gallery items should
    inherit it.
    """
    class Meta:
        abstract = True
        verbose_name = _("gallery item")

    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, blank=True, null=True)
    picture_name  = models.CharField(max_length=255, blank=True, default=u'')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    description   = models.TextField(blank=True, null=True)

    def get_filepath(self):
        """
        This method returns full pathname to item gallery. It may be useful for
        other custom views.
        """
        return str(settings.MEDIA_ROOT)

    def get_filename(self):
        """
        Returns full file path and filename.
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
            f = os.path.join(thumbs, str(s[0])+'x'+str(s[1])+'_' + filename)
            try:
                os.unlink(f)
            except Exception:
                pass
        try:
            os.unlink(self.get_filename())
        except Exception:
            pass
        super(GalleryItem, self).delete()

    def __unicode__(self):
        return self.picture_name   


class UserGalleryItem(GalleryItem):
    """
    This simple gallery item class handles user media.
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
        return self.get_thumbnail((128,128))

    def thumb_big(self):
        return self.get_thumbnail((256,256))

    def thumb_cropped(self):
        return settings.MEDIA_URL + self.user.username + '/cropped_' + self.picture_name


class LocationGalleryItem(GalleryItem):
    """
    This is basic class for items in location's gallery. File upload is handled
    other way, here we just add some additional data for our pictures, like
    comment and name.
    """
    location = models.ForeignKey(Location, related_name='pictures')
    
    class Meta:
        verbose_name = _("gallery item")

    def url(self):
        """
        Returns picture url. This function is most useful for views.
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

    def get_filepath(self):
        return str(os.path.join(settings.MEDIA_ROOT, self.location.slug))

    def get_absolute_url(self):
        return reverse('locations:picture',
                        kwargs={
                            'slug': self.location.slug,
                            'pk'  : self.pk,
                        })

    def __unicode__(self):
        return self.name or self.picture_name


models.signals.post_save.connect(crop_gallery_thumb, sender=UserGalleryItem)
models.signals.post_delete.connect(delete_cropped_thumb, sender=UserGalleryItem)
