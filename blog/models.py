# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from comments.models import CustomComment
from locations.models import Location
from taggit.managers import TaggableManager
# Activity stream
from django.db.models.signals import post_save
from actstream import action

class Category(models.Model):
    """
    User Blog Categories basic model
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    description = models.TextField(max_length=1024)
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug':self.slug})
    
    def __unicode__(self):
        return self.name

class News(models.Model):
    """
    Blog for Places
    """
    creator = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)
    content = models.TextField(max_length=10248, null=True, blank=True,)
    categories = models.ManyToManyField(
        Category,
        verbose_name=_('Categories'),
        null=True,
        blank=True,
    )
    location = models.ForeignKey(Location)
    tags = TaggableManager() #http://django-taggit.readthedocs.org/en/latest/

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:details', kwargs={'slug':self.slug})

    def get_comment_count(self):
        content_type = ContentType.objects.get_for_model(self)
        comments = CustomComment.objects.filter(object_pk=self.pk).filter(
                                                content_type=content_type)
        return len(comments)

    def get_entry_introtext(self):
        clean_content = strip_tags(self.content)
        return clean_content[:200] + '...'
    
    def __unicode__(self):
        return self.title

def create_entry_action_hook(sender, instance, created, **kwargs):
    """
    Action hook for activity stream when new blog entry is created
    """
    if created:
        action.send(
            instance.creator,
            action_object = instance,
            verb = 'posted',
            target = instance.location
        )

post_save.connect(create_entry_action_hook, sender=News)
    