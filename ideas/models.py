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

from actstream.actions import action
from taggit.managers import TaggableManager

from comments.models import CustomComment
from locations.models import Location
from gallery.image import adjust_uploaded_image
from notifications.models import notify
from places_core.helpers import truncatehtml, truncatesmart, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image


class VotingExpiredException(Exception):
    pass


@python_2_unicode_compatible
class Category(models.Model):
    """ """
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Idea(ImagableItemMixin, models.Model):
    """ """
    STATUS_CHOICES = ((1, _(u"active")), (2, _(u"in progress")),
                      (3, _(u"completed")), (4, _(u"project")), )

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
        ordering = ['name', ]
        verbose_name = _(u"idea")
        verbose_name_plural = _(u"ideas")

    def __str__(self):
        return self.name

    def check_access(self, user):
        access = user.is_authenticated()
        if not access:
            return False
        if user.is_superuser:
            access = True
        elif user == self.creator:
            access = True
        elif self.location in user.profile.mod_areas.all():
            access = True
        return access

    @property
    def votes_up(self):
        return self.vote_set.filter(status=1).count()

    @property
    def votes_down(self):
        return self.vote_set.filter(status=2).count()

    @property
    def note(self):
        if not self.vote_set.exclude(status=3).count():
            note = 0
        elif not self.votes_down:
            note = 100
        else:
            note = float(self.votes_up)/float(self.votes_down+self.votes_up)*100.0
        return "{}%".format(int(note))

    @property
    def votes(self):
        return self.vote_set.exclude(status=3).values('pk').count()

    def get_votes(self):
        return self.votes_up - self.votes_down

    def get_comment_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return CustomComment.objects.filter(object_pk=self.pk) \
                                    .filter(content_type=content_type) \
                                    .count()

    def vote(self, user, status=2):
        """ Semi-automatic voting. Just pass voting user and vote False/True.
        """
        # Voting is already disabled
        if self.status > 2:
            return {'success': False,
                    'message': _(u"Voting for this idea is over"), }

        try:
            user_vote = Vote.objects.get(user=user, idea=self)
            is_new = False
        except Vote.DoesNotExist:
            user_vote = Vote.objects.create(user=user, idea=self, status=status)
            is_new = True

        is_reversed = False

        if is_new:
            prev_status = None
            user.profile.rank_pts += 1
            user.profile.save()
        else:
            prev_status = user_vote.status
            if (prev_status == 2 and status == 1) or (prev_status == 1 and status == 2):
                is_reversed = True
        user_vote.status = status
        user_vote.save()

        vote_data = {
            'success': True,
            'id': user_vote.pk,
            'target': user_vote.status,
            'is_new': is_new,
            'prev_target': prev_status,
            'is_reversed': is_reversed,
            'votes': self.votes,
            'note': self.note, }

        return vote_data

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
        return reverse(
            'locations:idea_detail',
            kwargs={'slug': self.slug,
                    'place_slug': self.location.slug, })

    def get_description(self):
        return truncatehtml(self.description, 100)


models.signals.post_save.connect(adjust_uploaded_image, sender=Idea)
models.signals.post_delete.connect(remove_image, sender=Idea)


@python_2_unicode_compatible
class Vote(models.Model):
    """ Users can vote up or down on ideas. """
    VOTE_STATUSES = ((1, _(u"positive")),
                     (2, _(u"negative")),
                     (3, _(u"revoked")), )

    user = models.ForeignKey(User, related_name="idea_votes")
    idea = models.ForeignKey(Idea)
    status = models.PositiveIntegerField(choices=VOTE_STATUSES, default=2)
    date_voted = models.DateTimeField(auto_now=True)

    def status_display(self):
        return [[x[1] for x in VOTE_STATUSES if x[0]==self.status][0]]

    def __str__(self):
        return unicode(self.status)

    class Meta:
        unique_together = ('user', 'idea', )
        verbose_name = _(u"vote")
        verbose_name_plural = _(u"votes")


def vote_notification(sender, instance, created, **kwargs):
    """ Notify users that someone voted for their ideas. """
    if instance.user == instance.idea.creator or not created:
        return True
    suff = "up" if instance.status == 1 else "down"
    notify(instance.user, instance.idea.creator,
           key="vote",
           verb="voted for your idea",
           action_object=instance,
           action_target=instance.idea)


models.signals.post_save.connect(vote_notification, sender=Vote)
