# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from comments.models import CustomComment
from locations.models import Location
from taggit.managers import TaggableManager
from places_core.helpers import truncatehtml
# Generic bookmarks
from bookmarks.handlers import library


class Category(models.Model):
    """
    User Blog Categories basic model
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True, default="")
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug':self.slug})
    
    def __unicode__(self):
        return self.name


class News(models.Model):
    """
    Blog for Places
    """
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    content = models.TextField(max_length=10248, null=True, blank=True,)
    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
        null=True,
        blank=True,
    )
    location = models.ForeignKey(Location)
    edited = models.BooleanField(default=False)
    tags = TaggableManager() #http://django-taggit.readthedocs.org/en/latest/

    def save(self, *args, **kwargs):
        if self.pk:
            self.edited = True
        else:
            to_slug_entry = self.title
            try:
                chk = News.objects.filter(title=self.title)
                to_slug_entry = self.title + '-' + str(len(chk))
            except News.DoesNotExist:
                pass
            self.slug = slugify(to_slug_entry)
        super(News, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('locations:news_detail', kwargs={
            'place_slug': self.location.slug,
            'slug':self.slug,
        })

    def get_comment_count(self):
        content_type = ContentType.objects.get_for_model(self)
        comments = CustomComment.objects.filter(object_pk=self.pk).filter(
                                                content_type=content_type)
        return len(comments)

    def get_entry_introtext(self):
        clean_content = strip_tags(self.content)
        return clean_content[:200] + '...'

    def get_description(self):
        return truncatehtml(self.content, 100)
    
    def __unicode__(self):
        return self.title


# Allow users to bookmark content
library.register(News)
    