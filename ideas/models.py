# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from comments.models import CustomComment
from locations.models import Location
from taggit.managers import TaggableManager
from bookmarks.handlers import library


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
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(blank=True, null=True, auto_now=True)
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(max_length=20480, null=True, blank=True,)
    category = models.ForeignKey(Category, null=True, blank=True)
    location = models.ForeignKey(Location)
    status = models.BooleanField(default=True)
    # Track changes to mark item as edited when user changes it.
    edited = models.BooleanField(default=False)
    tags = TaggableManager()
    
    def get_votes(self):
        votes_total = self.vote_set
        votes_up = len(votes_total.filter(vote=True))
        votes_down = len(votes_total.filter(vote=False))
        return votes_up - votes_down

    def get_comment_count(self):
        content_type = ContentType.objects.get_for_model(self)
        comments = CustomComment.objects.filter(object_pk=self.pk).filter(
                                                content_type=content_type)
        return len(comments)

    def save(self, *args, **kwargs):
        if not self.pk:
            to_slug_entry = self.name
            chk = Idea.objects.filter(name=self.name)
            if len(chk) > 0:
                to_slug_entry = self.name + '-' + str(len(chk))
            self.slug = slugify(to_slug_entry)
        super(Idea, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('locations:idea_detail', kwargs={
            'slug':self.slug,
            'place_slug': self.location.slug,
        })
    
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


# Allow users to bookmark idea
library.register(Idea)
