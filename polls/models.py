# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slugify import slugify

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from ordered_model.models import OrderedModel
from taggit.managers import TaggableManager

from gallery.image import adjust_uploaded_image
from locations.models import Location
from places_core.helpers import truncatehtml, sanitizeHtml
from places_core.models import ImagableItemMixin, remove_image
from projects.models import SlugifiedModelMixin

from .managers import SimplePollResultsManager


@python_2_unicode_compatible
class Poll(ImagableItemMixin, models.Model):
    """ Base poll class - means entire poll.
    """
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    tags = TaggableManager()
    question = models.TextField()
    creator = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    multiple = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.title = strip_tags(self.title)
        self.question = sanitizeHtml(self.question)
        if not self.pk:
            to_slug_entry = self.title
            chk = Poll.objects.filter(title=self.title)
            if len(chk):
                to_slug_entry = self.title + '-' + str(len(chk))
            self.slug = slugify(to_slug_entry)
        super(Poll, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'locations:poll',
            kwargs={'place_slug': self.location.slug,
                    'slug': self.slug})

    def get_description(self):
        return truncatehtml(self.question, 100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', ]
        verbose_name = _(u"poll")
        verbose_name_plural = _(u"polls")


@python_2_unicode_compatible
class Answer(models.Model):
    """ Single answer model.
    """
    answer = models.CharField(max_length=256)
    poll = models.ForeignKey(Poll)

    def save(self, *args, **kwargs):
        self.answer = strip_tags(self.answer)
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return self.answer

    class Meta:
        ordering = ['answer', ]


class AnswerSet(models.Model):
    """ Remember user answers to generate some statistics.
    """
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    answers = models.ManyToManyField(Answer,
                                     related_name='answers',
                                     blank=True)


models.signals.post_save.connect(adjust_uploaded_image, sender=Poll)
models.signals.post_delete.connect(remove_image, sender=Poll)


@python_2_unicode_compatible
class SimplePoll(SlugifiedModelMixin):
    """ Stand-alone polls, not related to locations.
    """
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_(u"created at"))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SimplePollQuestion(OrderedModel):
    """ Form widgets choices are dependent on question type.
    """
    QUESTION_TYPES = ((1, _(u"single")), (2, _(u"multiple")),
                      (3, _(u"opened")), )
    text = models.TextField(default="", verbose_name=_(u"question"))
    polls = models.ManyToManyField(SimplePoll,
                                   blank=True,
                                   null=True,
                                   verbose_name=_(u"polls"))
    question_type = models.PositiveIntegerField(choices=QUESTION_TYPES,
                                                default=1,
                                                verbose_name=_(u"type"))

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class SimplePollAnswer(OrderedModel):
    """ Represents answsers for single and multiple questions.
    """
    text = models.CharField(max_length=255,
                            default="",
                            verbose_name=_(u"answer"))
    question = models.ForeignKey(SimplePollQuestion,
                                 blank=True,
                                 null=True,
                                 verbose_name=_(u"question"))

    order_with_respect_to = 'question'

    def __str__(self):
        return self.text


@python_2_unicode_compatible
class SimplePollAnswerSet(models.Model):
    """ Answer set - one user, one poll try.
    """
    user = models.ForeignKey(User, verbose_name=_(u"user"))
    poll = models.ForeignKey(SimplePoll, verbose_name=_(u"poll"))
    question = models.ForeignKey(SimplePollQuestion,
                                 verbose_name=_(u"question"))
    answer = models.TextField(default="", verbose_name=_(u"answer"))
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = SimplePollResultsManager()

    def __str__(self):
        return u"answer set for %s" % self.poll

    class Meta:
        unique_together = ('user', 'poll', 'question', )
