# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Activity stream
from django.db.models.signals import post_save
from actstream import action
# Override system storage: 
#http://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file
from places_core.storage import OverwriteStorage


class Location(models.Model):
    """
    Basic location model
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(max_length=10000, blank=True)
    latitude  = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    creator   = models.ForeignKey(User, blank=True, related_name='created_locations')
    users     = models.ManyToManyField(User, blank=True)
    parent    = models.ForeignKey('Location', blank=True, null=True)
    image     = models.ImageField(
        upload_to = 'img/locations/',
        default = 'img/locations/nowhere.jpg',
        storage = OverwriteStorage()
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    def get_parent_chain(self, parents=None):
        """
        Take all parent location in 'chain' of name - url pairs.
        """
        if parents == None:
            parents = []
        if self.parent:
            parents.append({
                'name': self.parent.name,
                'url' : self.parent.get_absolute_url(),
            })
            if self.parent.parent:
                self.parent.get_parent_chain(parents)
        return reversed(parents)

    def get_absolute_url(self):
        return reverse('locations:details', kwargs={'slug':self.slug})
    
    def __unicode__(self):
        return self.name


def create_place_action_hook(sender, instance, created, **kwargs):
    """
    Action hook for activity stream when new place is created
    TODO - move it to more appropriate place.
    """
    if created:
        instance.users.add(instance.creator)
        action.send(instance.creator, action_object=instance, verb='created')

post_save.connect(create_place_action_hook, sender=Location)
