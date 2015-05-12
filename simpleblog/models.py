# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from gallery.image import adjust_uploaded_image
from places_core.helpers import sanitizeHtml
from places_core.models import ImagableItemMixin
from projects.models import SlugifiedModelMixin

from .signals import blog_entry_created_action


class BlogManager(models.Manager):
    """
    This manager simplifies process of filtering content tied to specific
    objects or users.
    """
    def get_published_in(self, obj):
        """
        Return list of blog entries published (tied to) given object.
        """
        ct = ContentType.objects.get_for_model(obj).pk
        return super(BlogManager, self).get_queryset()\
            .filter(content_type__id=ct, object_id=obj.pk)

    def get_published_by(self, user):
        """
        Return all blog entries created by given user.
        """
        return super(BlogManager, self).get_queryset().filter(author=user)


@python_2_unicode_compatible
class BlogCategory(models.Model):
    """
    Every blog entry may optionally fall into one category.
    """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u"blog category")
        verbose_name_plural = _(u"blog categories")


@python_2_unicode_compatible
class BlogEntry(SlugifiedModelMixin, ImagableItemMixin):
    """
    Basic class for simplified blog entries. Blog entry may be tied to another
    content, for example organization, project or location. This way we can use
    custom managers to filter content from such modules.
    """
    content = models.TextField(default="", verbose_name=_(u"content"))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_(u"date created"))
    date_edited = models.DateTimeField(auto_now=True,
                                       verbose_name=_(u"date edited"))
    author = models.ForeignKey(User,
                               related_name="simpleblog_entries",
                               verbose_name=_(u"author"))
    category = models.ForeignKey(BlogCategory,
                                 blank=True,
                                 null=True,
                                 verbose_name=_(u"category"))
    tags = models.CharField(default="",
                            blank=True,
                            max_length=255,
                            verbose_name=_(u"tags"),
                            help_text=_(u"List of tags separated by comma"))

    # By defining generic relation we can decide where to publish this entry
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = BlogManager()

    def get_absolute_url(self):
        if self.content_object is not None:
            model_name = self.content_object._meta.model_name
            if model_name == 'organization':
                return reverse('organizations:news-detail', kwargs={
                    'slug': self.content_object.slug,
                    'news_slug': self.slug, })
            elif model_name == 'idea':
                return reverse('locations:idea-news-list', kwargs={
                    'location_slug': self.content_object.location.slug,
                    'slug': self.content_object.slug, })
        return reverse('simpleblog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.content = sanitizeHtml(self.content)
        super(BlogEntry, self).save(*args, **kwargs)

    def has_access(self, user):
        """ Check if particular user can delete/update this entry. """
        if user.is_superuser:
            return True
        return user == self.author

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created', ]
        verbose_name = _(u"blog entry")
        verbose_name_plural = _(u"blog entries")


models.signals.post_save.connect(blog_entry_created_action, sender=BlogEntry)
models.signals.post_save.connect(adjust_uploaded_image, sender=BlogEntry)
