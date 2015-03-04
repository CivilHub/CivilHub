# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from slugify import slugify

from django.db import models, transaction
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from taggit.managers import TaggableManager

from comments.models import CustomComment
from locations.models import Location
from gallery.image import adjust_uploaded_image
from places_core.helpers import truncatehtml, truncatesmart, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image


@python_2_unicode_compatible
class Category(models.Model):
    """
    User Idea Categories basic model
    """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


@python_2_unicode_compatible
class Idea(ImagableItemMixin, models.Model):
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
        votes_up = self.vote_set.filter(vote=True).count()
        votes_down = self.vote_set.filter(vote=False).count()
        return votes_up - votes_down

    def get_comment_count(self):
        content_type = ContentType.objects.get_for_model(self)
        comments = CustomComment.objects.filter(object_pk=self.pk).filter(
                                                content_type=content_type)
        return len(comments)

    def save(self, *args, **kwargs):
        self.name = strip_tags(self.name)
        if len(self.name) >= 64:
            self.name = truncatesmart(self.name, 60)
        self.description = sanitizeHtml(self.description)

        slug = slugify(self.name)
        self.slug = slug
        success = False
        retries = 0
        while not success:
            check = self.__class__.objects.filter(slug=self.slug)\
                                          .exclude(pk=self.pk).count()
            if not check:
                success = True
            else:
                # We assume maximum number of 50 elements with the same name.
                # But the loop should be breaked if something went wrong.
                if retries >= 50:
                    raise ValidationError(u"Maximum number of retries exceeded")
                retries += 1
                self.slug = "{}-{}".format(slug, retries)
        super(Idea, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('locations:idea_detail', kwargs={
            'slug':self.slug,
            'place_slug': self.location.slug,
        })
        
    def get_description(self):
        return truncatehtml(self.description, 100)

    @transaction.autocommit
    def delete(self):
        """
        Customowa metoda do usuwania jest najwyraźniej niezbędna we wszystkich
        modelach korzystających z django-taggit. Powodem jest błąd w pluginie,
        który powoduje błędy transakcji.

        FIXME: możliwe, że to już jest niepotrzebne
        """
        with transaction.autocommit():
            super(Idea, self).delete()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


@python_2_unicode_compatible
class Vote(models.Model):
    """
    Users can vote up or down on ideas
    """
    user = models.ForeignKey(User)
    idea = models.ForeignKey(Idea)
    vote = models.BooleanField(default=False)
    date_voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


models.signals.post_save.connect(adjust_uploaded_image, sender=Idea)
models.signals.post_delete.connect(remove_image, sender=Idea)
