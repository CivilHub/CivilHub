# -*- coding: utf-8 -*-
import operator
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from actstream.models import model_stream
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
    population= models.IntegerField(blank=True, null=True)
    image     = models.ImageField(
        upload_to = 'img/locations/',
        default = 'img/locations/nowhere.jpg',
        storage = OverwriteStorage()
    )


    def save(self, *args, **kwargs):
        if not self.pk:
            to_slug_entry = self.name
            chk = Location.objects.filter(slug=slugify(self.name))
            if len(chk) > 0:
                to_slug_entry = self.name + '-' + str(len(chk))
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


    def get_ancestor_chain(self, ancestors=None):
        """
        Get all sublocations and return dictionary of name - url pairs.
        """
        if ancestors == None:
            ancestors = []
        for a in self.location_set.all():
            ancestors.append({
                'name': a.name,
                'url' : a.get_absolute_url(),
            })
            if a.location_set.count() > 0:
                a.get_ancestor_chain(ancestors)
        return ancestors


    def count_users_actions(self, user):
        """
        Count actions related to this place performed
        by particular provided user.
        """
        ct = ContentType.objects.get_for_model(User)
        pk = user.pk
        target_ct = ContentType.objects.get_for_model(self)
        stream = model_stream(self)
        actions = stream.filter(target_content_type=target_ct)
        actions = actions.filter(actor_content_type=ct)
        actions = actions.filter(actor_object_id=pk)
        actions = actions.filter(target_object_id=self.pk)
        return actions.count()


    def most_active_followers(self, limit=10):
        """ Show the most active followers of current place. """
        tmp = []
        for user in self.users.all():
            tmp.append({
                'user' : user,
                'count': self.count_users_actions(user),
            })
        tmp = sorted(tmp, key=operator.itemgetter('count'))
        actions = reversed(tmp)

        return actions


    def get_absolute_url(self):
        return reverse('locations:details', kwargs={'slug':self.slug})


    def __unicode__(self):
        return self.name
