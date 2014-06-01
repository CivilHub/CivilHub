from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from locations.models import Location
from bookmarks.handlers import library


class Category(models.Model):
    """
    Basic categories for forum discussions
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True, default="")

    def __unicode__(self):
        return self.name


class Discussion(models.Model):
    """
    Single discussion on forum - e.g. some topic.
    """
    question = models.CharField(max_length=256)
    slug     = models.SlugField(max_length=256)
    intro    = models.TextField()
    creator  = models.ForeignKey(User)
    status   = models.BooleanField(default=True)
    location = models.ForeignKey(Location)
    category = models.ForeignKey(Category, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(Discussion, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locations:topic',
            kwargs={
                'place_slug':self.location.slug,
                'slug': self.slug,
            }
        )

    def __unicode__(self):
        return self.question


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
        if self.pk is not None:
            self.is_edited = True
        super(Entry, self).save(*args, **kwargs)


# Allow users to bookmark content
library.register(Discussion)
