# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from locations.models import Location

class Idea(models.Model):
    """
    User Idea basic model
    """
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    location = models.ForeignKey(Location)
    # TODO implement Django tag system
    tags = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    
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
