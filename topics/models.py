# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slugify import slugify

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from gallery.image import adjust_uploaded_image
from locations.models import Location
from notifications.models import notify
from places_core.helpers import truncatehtml, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image


@python_2_unicode_compatible
class Category(models.Model):
    """
    Basic categories for forum discussions
    """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]


@python_2_unicode_compatible
class Discussion(ImagableItemMixin, models.Model):
    """
    Single discussion on forum - e.g. some topic.
    """
    question = models.CharField(max_length=255)
    slug     = models.SlugField(max_length=255, unique=True)
    intro    = models.TextField()
    creator  = models.ForeignKey(User)
    status   = models.BooleanField(default=True)
    location = models.ForeignKey(Location)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags     = TaggableManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.question = strip_tags(self.question)
        self.intro = sanitizeHtml(self.intro)
        if not self.slug:
            to_slug_entry = self.question
            chk = Discussion.objects.filter(question=self.question)
            if len(chk) > 0:
                to_slug_entry = self.question + '-' + str(len(chk))
            self.slug = slugify(to_slug_entry)
        super(Discussion, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locations:topic',
            kwargs={
                'place_slug':self.location.slug,
                'slug': self.slug,
            }
        )

    def get_description(self):
        return truncatehtml(self.intro, 100)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['question',]
        verbose_name = _(u"discussion")
        verbose_name_plural = _(u"discussions")


class Entry(MPTTModel):
    """
    Single forum entry.
    """
    content = models.TextField()
    creator = models.ForeignKey(User)
    discussion   = models.ForeignKey(Discussion)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited  = models.DateTimeField(auto_now=True)
    is_edited    = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    class MPTTMeta:
        order_insertion_by = ['date_created']

    def save(self, *args, **kwargs):
        self.content = sanitizeHtml(self.content)
        if self.pk is not None:
            self.is_edited = True
        super(Entry, self).save(*args, **kwargs)

    def get_upvotes(self):
        return len(self.votes.filter(vote=True))

    def get_downvotes(self):
        return len(self.votes.filter(vote=False))

    def calculate_votes(self):
        votes_total = self.votes
        votes_up = len(votes_total.filter(vote=True))
        votes_down = len(votes_total.filter(vote=False))
        return votes_up - votes_down

    def get_absolute_url(self):
        return self.discussion.get_absolute_url()

    class Meta:
        ordering = ['-date_created',]


@python_2_unicode_compatible
class EntryVote(models.Model):
    """
    Users can vote up or down on forum entries, but only once.
    """
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)
    entry = models.ForeignKey(Entry, related_name='votes')
    date_voted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return unicode(self.vote)


# Signals
# ------------------------------------------------------------------------------


def response_notification(sender, instance, created, **kwargs):
    """ Notify discussion creator about every new answer. """
    if not created or instance.creator == instance.discussion.creator:
        return True
    notify(instance.creator, instance.discussion.creator,
        key="answer",
        verb=_(u"answered for your discussion"),
        action_object=instance,
        action_target=instance.discussion
    )
models.signals.post_save.connect(response_notification, sender=Entry)


def vote_notification(sender, instance, created, **kwargs):
    """ Notify entry author about votes for his/her entry. """
    if not created:
        return True
    suff = "up" if instance.vote else "down"
    notify(instance.user, instance.entry.creator,
        key="vote",
        verb=_(u"voted for %s your entry" % suff),
        action_object=instance,
        action_target=instance.entry
    )
models.signals.post_save.connect(vote_notification, sender=EntryVote)


# External signals
# ------------------------------------------------------------------------------


models.signals.post_save.connect(adjust_uploaded_image, sender=Discussion)
models.signals.post_delete.connect(remove_image, sender=Discussion)
