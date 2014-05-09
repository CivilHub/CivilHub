from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
    """
    Basic categories for forum discussions
    """
    name = models.CharField(max_length=64)
    description = models.TextField()


class Discussion(models.Model):
    """
    Single discussion on forum - e.g. some topic.
    """
    question = models.CharField(max_length=256)
    slug     = models.SlugField(max_length=256)
    creator  = models.ForeignKey(User)
    status   = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Discussion, self).save(*args, **kwargs)


class Entry(MPTTModel):
    """
    Single forum entry.
    """
    content = models.TextField()
    creator = models.ForeignKey(User)
    discussion   = models.ForeignKey(Discussion)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited  = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    class MPTTMeta:
        order_insertion_by = ['submit_date']
