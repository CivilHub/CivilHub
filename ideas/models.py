# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from locations.models import Location
from taggit.managers import TaggableManager

class Category(models.Model):
    """
    User Idea Categories basic model
    """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    
    def __unicode__(self):
        return self.name

class Idea(models.Model):
    """
    User Idea basic model
    """
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True,)
    categories = models.ManyToManyField(Category, verbose_name='Kategorie', null=True, blank=True,)
    location = models.ForeignKey(Location)
    # TODO implement Django tag system
    tags = TaggableManager() #http://django-taggit.readthedocs.org/en/latest/
    
    def get_absolute_url(self):
        return reverse('ideas:details', kwargs={'pk':self.pk})
    
    def __unicode__(self):
        return self.name
        
    
class Vote(models.Model):
    """
    Users can vote up or down on ideas
    """
    user = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    vote = models.BooleanField(default=False)
    date_voted = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.vote
