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
from notifications.models import notify
from places_core.helpers import truncatehtml, truncatesmart, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image


@python_2_unicode_compatible
class Category(models.Model):
    """ """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Idea(ImagableItemMixin, models.Model):
    """ """
    STATUS_CHOICES = (
        (1, _(u"active")),
        (2, _(u"completed")),
        (3, _(u"in progress")),
        (4, _(u"project")),
    )

    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(blank=True, null=True, auto_now=True)
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=70, unique=True)
    description = models.TextField(blank=True, default="")
    category = models.ForeignKey(Category, null=True, blank=True)
    location = models.ForeignKey(Location)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)
    edited = models.BooleanField(default=False)

    tags = TaggableManager()

    class Meta:
        ordering = ['name',]
        verbose_name = _(u"idea")
        verbose_name_plural = _(u"ideas")

    def __str__(self):
        return self.name

    def get_votes(self):
        votes_up = self.vote_set.filter(vote=True).count()
        votes_down = self.vote_set.filter(vote=False).count()
        return votes_up - votes_down

    def get_comment_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return CustomComment.objects.filter(object_pk=self.pk) \
                                    .filter(content_type=content_type) \
                                    .count()

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


models.signals.post_save.connect(adjust_uploaded_image, sender=Idea)
models.signals.post_delete.connect(remove_image, sender=Idea)


@python_2_unicode_compatible
class Vote(models.Model):
    """ Users can vote up or down on ideas. """
    user = models.ForeignKey(User, related_name="idea_votes")
    idea = models.ForeignKey(Idea)
    vote = models.BooleanField(default=False)
    date_voted = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'idea',)
        verbose_name = _(u"vote")
        verbose_name_plural = _(u"votes")

    def __str__(self):
        if self.vote:
            return _(u"positive")
        else:
            return _(u"negative")


def vote_notification(sender, instance, created, **kwargs):
    """ Notify users that someone voted for their ideas. """
    if instance.user == instance.idea.creator or not created:
        return True
    suff = "up" if instance.vote else "down"
    notify(instance.user, instance.idea.creator,
        key="vote",
        verb=_(u"voted %s for your idea" % suff),
        action_object=instance,
        action_target=instance.idea
    )
models.signals.post_save.connect(vote_notification, sender=Vote)
