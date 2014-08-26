# -*- coding: utf-8 -*-
import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from locations.models import Location


class GalleryItem(models.Model):
    """
    Basic abstract model for gallery items. All types of gallery items should
    inherit it.
    """
    class Meta:
        abstract = True
        verbose_name = _("gallery item")

    user = models.ForeignKey(User)
    picture_name  = models.CharField(max_length=255, blank=True, default=u'')
    date_uploaded = models.DateTimeField(auto_now_add=True)

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


class LocationGalleryItem(GalleryItem):
    """
    This is basic class for items in location's gallery. File upload is handled
    other way, here we just add some additional data for our pictures, like
    comment and name.
    """
    name = models.CharField(max_length=64, blank=True, null=True)
    location = models.ForeignKey(Location, related_name='pictures')
    description = models.TextField(blank=True, null=True)
    
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
