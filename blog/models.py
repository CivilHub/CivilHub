# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slugify import slugify

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from comments.models import CustomComment
from locations.models import Location
from gallery.image import adjust_uploaded_image
from notifications.models import notify
from places_core.helpers import truncatehtml, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image


@python_2_unicode_compatible
class Category(models.Model):
    """ """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(max_length=1024, blank=True, null=True, default="")

    class Meta:
        ordering = ['name',]
        verbose_name = _(u"category")
        verbose_name_plural = _(u"categories")

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_entry = self.name
            chk = Category.objects.filter(slug=slugify(slug_entry))
            if len(chk): slug_entry = slug_entry + "-" + str(len(chk))
            self.slug = slugify(slug_entry)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class News(ImagableItemMixin):
    """ """
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64, verbose_name=_(u"title"))
    slug = models.SlugField(max_length=64, unique=True)
    content = models.TextField(max_length=10248, null=True, blank=True, verbose_name=_(u"content"))
    category = models.ForeignKey(Category, verbose_name=_(u'category'), null=True, blank=True)
    location = models.ForeignKey(Location)
    edited = models.BooleanField(default=False)

    tags = TaggableManager()

    class Meta:
        ordering = ['title',]
        verbose_name = _(u"news")
        verbose_name_plural = _(u"newses")

    def save(self, *args, **kwargs):
        self.title = strip_tags(self.title)
        self.content = sanitizeHtml(self.content)
        if self.pk:
            self.edited = True
        slug = slugify(self.title)
        if not self.slug:
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
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locations:news_detail', kwargs={
            'location_slug': self.location.slug,
            'slug':self.slug,
        })

    def get_comment_count(self):
        """ Returns the number of comments for a single entry. """
        content_type = ContentType.objects.get_for_model(self)
        return CustomComment.objects.filter(object_pk=self.pk)\
                                    .filter(content_type=content_type)\
                                    .count()

    def get_entry_introtext(self):
        clean_content = strip_tags(self.content)
        return clean_content[:200] + '...'

    def get_description(self):
        return truncatehtml(self.content, 100)

    def __str__(self):
        return self.title


def notify_about_news_deletion(sender, instance, **kwargs):
    """ Notify newss author about that his news was deleted. """
    # For now we assume that only superuser could delete news entries.
    admin = User.objects.filter(is_superuser=True)[0]
    notify(admin, instance.creator,
        key="deletion",
        verb="deleted your blog entry",
        action_object=instance
    )
#models.signals.post_delete.connect(notify_about_news_deletion, sender=News)
models.signals.post_save.connect(adjust_uploaded_image, sender=News)
models.signals.post_delete.connect(remove_image, sender=News)
