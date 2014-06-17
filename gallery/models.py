# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class LocationGalleryItem(models.Model):
    """
    This is basic class for items in location's gallery. File upload is handled
    other way, here we just add some additional data for our pictures, like
    comment and name.
    """
    name = models.CharField(max_length=64, blank=True, null=True)
    user = models.ForeignKey(User)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    picture_name  = models.CharField(max_length=256)
    description   = models.TextField(blank=True, null=True)

    def get_thumbnail(self, size):
        """
        This function returns url to thumbnail of photo. Size parameter is man-
        datory and related to thumb sizes declared in views module. It should
        be touple or list containing images width and height.
        """
        return str(size[0]) + 'x' + str(size[1]) + self.picture_name

    def __unicode__(self):
        return self.name
