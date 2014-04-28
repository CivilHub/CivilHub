# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from locations.models import Location
from taggit.managers import TaggableManager

class Category(models.Model):
    """
    User Blog Categories basic model
    """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    
    def __unicode__(self):
        return self.name

class News(models.Model):
    """
    Blog for Places
    """
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=10240, null=True, blank=True,)
    categories = models.ManyToManyField(Category, verbose_name='Kategorie', null=True, blank=True,)
    location = models.ForeignKey(Location)
    tags = TaggableManager() #http://django-taggit.readthedocs.org/en/latest/
    
    def get_absolute_url(self):
        return reverse('blog:details', kwargs={'pk':self.pk})
    
    def __unicode__(self):
        return self.title
        
    