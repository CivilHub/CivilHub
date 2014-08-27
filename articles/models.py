# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """ """
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class Article(models.Model):
    """ """
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    def get_absolute_url(self):
        if self.category:
            return reverse('articles:'+self.category.name_en.lower()+'_entry',
                            kwargs={'slug':self.slug})
        return '/' + self.slug + '/'

    def __unicode__(self):
        return self.title
