from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from slugify import slugify
from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from locations.models import Location
from places_core.helpers import truncatehtml, sanitizeHtml


class Category(models.Model):
    """
    Basic categories for forum discussions
    """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True, default="")

    def __unicode__(self):
        return self.name


class Discussion(models.Model):
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

    def __unicode__(self):
        return self.question
    
    class Meta:
        verbose_name = _("discussion")


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


class EntryVote(models.Model):
    """
    Users can vote up or down on forum entries, but only once.
    """
    user = models.ForeignKey(User)
    vote = models.BooleanField(default=False)
    entry = models.ForeignKey(Entry, related_name='votes')
    date_voted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.vote
