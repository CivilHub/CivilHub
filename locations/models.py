# -*- coding: utf-8 -*-
from django.db import models

class Location(models.Model):
    """
    Basic location model
    """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(
        upload_to = "img/locations/",
        default = 'img/locations/nowhere.png'
    )
    
    def __unicode__(self):
        return self.name
