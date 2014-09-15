from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from locations.models import Location
from taggit.managers import TaggableManager
from places_core.helpers import truncatehtml, sanitizeHtml


class Poll(models.Model):
    """
    Base poll class - means entire poll.
    """
    title = models.CharField(max_length=128)
    slug  = models.SlugField(max_length=128, unique=True)
    tags  = TaggableManager()
    question = models.TextField()
    creator  = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    multiple = models.BooleanField(default=False)
    date_created  = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.question = sanitizeHtml(self.question)
        if not self.pk:
            to_slug_entry = self.title
            chk = Poll.objects.filter(title=self.title)
            if len(chk):
                to_slug_entry = self.title + '-' + str(len(chk))
            self.slug = slugify(to_slug_entry)
        super(Poll, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locations:poll',
            kwargs={
                'place_slug':self.location.slug,
                'slug': self.slug
            }
        )

    def get_description(self):
        return truncatehtml(self.question, 100)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    """
    Single answer model.
    """
    answer = models.CharField(max_length=256)
    poll   = models.ForeignKey(Poll)

    def save(self, *args, **kwargs):
        self.answer = sanitizeHtml(self.answer)
        super(Answer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.answer


class AnswerSet(models.Model):
    """
    Remember user answers to generate some statistics.
    """
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    answers = models.ManyToManyField(Answer, related_name='answers', blank=True)
