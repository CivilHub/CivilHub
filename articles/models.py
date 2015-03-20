# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey


@python_2_unicode_compatible
class Category(MPTTModel):
    """ Nested category model. """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


@python_2_unicode_compatible
class Article(models.Model):
    """ Basic model for different types of articles. """
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    subtitle = models.CharField(max_length=200, blank=True, default="", verbose_name=_(u"subtitle"))
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    def get_absolute_url(self):
        """ 
        We have to treat support entries differently then others. It's possible
        to add support for nested categories and link them to urls if this will
        be desired.
        """
        if self.category is None or not self.category.name in ['Blog', 'Support']:
            category = None
        else:
            category = self.category.name.lower()
        if category is None:
            # stand-alone article - remember to configure urls properly!!!
            return '/' + self.slug + '/'
        elif category == 'support':
            # wpisy w kategorii 'support' traktowane są unikalnie
            urlentry = 'articles:support_entry'
        elif category == 'blog':
            # wpisy na blogu
            urlentry = 'articles:blog_entry'
        return reverse(urlentry.lower(), kwargs={'slug':self.slug})
        

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title',]
