# -*- coding: utf-8 -*-
from slugify import slugify

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from comments.models import CustomComment
from locations.models import Location
from places_core.helpers import truncatehtml, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image


class Category(models.Model):
    """
    User Blog Categories basic model
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True, default="")
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_entry = self.name
            chk = Category.objects.filter(slug=slugify(slug_entry))
            if len(chk): slug_entry = slug_entry + "-" + str(len(chk))
            self.slug = slugify(slug_entry)
        super(Category, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = _("category"),
        verbose_name_plural = _("categories")


class News(ImagableItemMixin, models.Model):
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
        verbose_name=_('category'),
        null=True,
        blank=True,
    )
    location = models.ForeignKey(Location)
    edited = models.BooleanField(default=False)
    tags = TaggableManager() #http://django-taggit.readthedocs.org/en/latest/

    def save(self, *args, **kwargs):
        self.title = strip_tags(self.title)
        self.content = sanitizeHtml(self.content)
        if self.pk:
            self.edited = True
        else:
            to_slug_entry = self.title
            chk = News.objects.filter(title=self.title)
            if len(chk):
                to_slug_entry = self.title + '-' + str(len(chk))
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

    class Meta:
        ordering = ['title',]
        verbose_name = _("news"),
        verbose_name_plural = _("news")


models.signals.post_delete.connect(remove_image, sender=News)
