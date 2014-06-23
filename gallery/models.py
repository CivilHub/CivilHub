# -*- coding: utf-8 -*-
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from locations.models import Location


class LocationGalleryItem(models.Model):
    """
    This is basic class for items in location's gallery. File upload is handled
    other way, here we just add some additional data for our pictures, like
    comment and name.
    """
    name = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location, related_name='pictures')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    picture_name  = models.CharField(max_length=256)
    description   = models.TextField(blank=True, null=True)

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
        super(LocationGalleryItem, self).delete()

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
        """
        This method returns full pathname to item gallery. It may be useful for
        other custom views.
        """
        return str(os.path.join(settings.MEDIA_ROOT, self.location.slug))

    def get_filename(self):
        """
        Returns full file path and filename.
        """
        path = self.get_filepath()
        return os.path.join(path, self.picture_name)

    def __unicode__(self):
        return self.name or self.picture_name
