# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Override system storage: 
#http://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file
from places_core.storage import OverwriteStorage


class Location(models.Model):
    """
    Basic location model
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
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
        to_slug_entry = self.name
        try:
            chk = Location.objects.filter(name=self.name)
            to_slug_entry = self.name + '-' + str(len(chk))
        except Location.DoesNotExist:
            pass
        self.slug = slugify(to_slug_entry)
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


    def get_ancestor_chain(self):
        """
        Get all sublocations and return dictionary of name - url pairs.
        """
        ancestors = []
        for a in self.location_set.all():
            ancestors.append({
                'name': a.name,
                'url' : a.get_absolute_url(),
            })
        return reversed(ancestors)


    def get_absolute_url(self):
        return reverse('locations:details', kwargs={'slug':self.slug})


    def __unicode__(self):
        return self.name
