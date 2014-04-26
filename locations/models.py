# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Location(models.Model):
    """
    Basic location model
    """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    creator = models.ForeignKey(User, blank=True, related_name='created_locations')
    users = models.ManyToManyField(User, blank=True)
    image = models.ImageField(
        upload_to = 'img/locations/',
        default = 'img/locations/nowhere.jpg'
    )
    
    def get_absolute_url(self):
        return reverse('locations:details', kwargs={'pk':self.pk})
    
    def __unicode__(self):
        return self.name
