# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes
import os
from slugify import slugify
from uuid import uuid4

from django.db import models
from django.utils.html import strip_tags
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ordered_model.models import OrderedModel

from etherpad.models import EtherpadGroup, EtherpadAuthor
from gallery.image import resize_background_image
from ideas.models import Idea
from locations.models import Location, BackgroundModelMixin
from mapvotes.models import Voting
from places_core.helpers import sanitizeHtml

from places_core.helpers import truncatehtml

from .signals import project_created_action, project_task_action


def get_upload_path(instance, filename):
    """ I set a path and a random name for the background image of the project. """
    return 'img/projects/' + uuid4().hex + os.path.splitext(filename)[1]


def get_attachment_path(instance, filename):
    """ Same as above, but for attachment files.
    """
    return 'attachments/' + uuid4().hex + os.path.splitext(filename)[1]


class SlugifiedModelMixin(models.Model):
    """
    Provides 'clean' slug for this object, adding number of such
    elements to base name. Additionaly, we sanitize input from user.
    """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    slug = models.CharField(max_length=210, verbose_name=_(u"slug"))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.name = strip_tags(self.name)
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
        super(SlugifiedModelMixin, self).save(*args, **kwargs)


MODULE_CHOICES = (
    (1, _(u"Mapvotes")),
    (2, _(u"Documents")),
    (3, _(u"News")),
    (4, _(u"Discussion")),
    (5, _(u"Gallery")),
)


@python_2_unicode_compatible
class SocialProject(BackgroundModelMixin, SlugifiedModelMixin):
    """ """
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    location = models.ForeignKey(Location, verbose_name=_(u"location"), related_name="projects")
    participants = models.ManyToManyField(User, verbose_name=_(u"participants"), blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_(u"date changed"))
    is_done = models.BooleanField(default=False, verbose_name=_(u"finished"))
    creator = models.ForeignKey(User, verbose_name=_(u"created by"), related_name="projects")
    image = models.ImageField(blank=True, upload_to=get_upload_path, default='img/projects/default.jpg')
    # Etherpad lite authors group allows us to handle documents for project
    authors_group = models.ForeignKey(EtherpadGroup, null=True, blank=True)
    # Ideas may be converted into projects. In this case we need this relation
    idea = models.ForeignKey(Idea, blank=True, null=True,
                             related_name='projects',
                             verbose_name=_(u"idea"))
    modules = models.TextField(_(u"modules"), default='2,3,4,5')

    class Meta:
        verbose_name = _(u"project")
        verbose_name_plural = _(u"projects")

    @property
    def votings(self):
        return Voting.objects.get_for_instance(self)

    @property
    def enabled_modules(self):
        modules = [int(x.strip()) for x in self.modules.split(',')]
        return modules

    @property
    def progress(self):
        """
        Returns a approximated percentage value of how "advanced" the project it.
        The way of counting this is very simple. we take the average of
        the completed tasks.
        """
        all_tasks = sum([group.task_set.count() for group in self.taskgroup_set.all()])
        finished_tasks = sum([group.task_set.filter(is_done=True).count()\
                              for group in self.taskgroup_set.all()])
        if not finished_tasks:
            return 0
        return int(float(finished_tasks) / float(all_tasks) * 100)

    @property
    def image_url(self):
        # Legacy method - we need it to simplify serialization
        # process when fetching contents from locations.
        return self.image.url

    @property
    def thumbnail(self):
        # Another legacy method for serializer.
        return self.thumb_url()

    def get_description(self):
        return truncatehtml(self.description, 100)

    def get_absolute_url(self):
        return reverse('locations:project_details', kwargs={
            'location_slug': self.location.slug,
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        self.description = sanitizeHtml(self.description)
        if not self.authors_group:
            self.authors_group = EtherpadGroup.objects.create(name=self.name)
        super(SocialProject, self).save(*args, **kwargs)

    def destroy(self):
        self.authors_group.delete()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TaskGroup(OrderedModel):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    project = models.ForeignKey(SocialProject, verbose_name=_(u"project"))
    creator = models.ForeignKey(User, verbose_name=_(u"created by"), related_name="task_groups")

    order_with_respect_to = 'project'

    class Meta:
        ordering = ['order',]
        verbose_name = _(u"task group")
        verbose_name_plural = _(u"task groups")

    def save(self, *args, **kwargs):
        self.name = strip_tags(self.name)
        self.description = sanitizeHtml(self.description)
        super(TaskGroup, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Task(OrderedModel):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    group = models.ForeignKey(TaskGroup, verbose_name=_(u"group"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_(u"date changed"))
    date_limited = models.DateTimeField(blank=True, null=True, verbose_name=_(u"time limit"))
    participants = models.ManyToManyField(User, verbose_name=_(u"participants"), blank=True, null=True)
    is_done = models.BooleanField(default=False, verbose_name=_(u"finished"))
    creator = models.ForeignKey(User, verbose_name=_(u"created by"), related_name="tasks")

    order_with_respect_to = 'group'

    class Meta:
        ordering = ['order',]
        verbose_name = _(u"task")
        verbose_name_plural = _(u"tasks")

    def save(self, *args, **kwargs):
        self.name = strip_tags(self.name)
        self.description = sanitizeHtml(self.description)
        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('locations:task_details', kwargs={
            'location_slug': self.group.project.location.slug,
            'slug': self.group.project.slug,
            'task_id': self.pk
        })

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class SocialForumTopic(SlugifiedModelMixin):
    """ Każda instancja to poszczególny temat na forum. """
    project = models.ForeignKey(SocialProject, verbose_name=_(u"project"), related_name="discussions")
    description = models.TextField(verbose_name=_(u"description"), default="", blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_("date edited"))
    is_closed = models.BooleanField(default=False, verbose_name=_(u"closed"), blank=True)
    creator = models.ForeignKey(User, verbose_name=_(u"creator"), related_name="social_topics")

    class Meta:
        verbose_name = (u"discussion")
        verbose_name_plural = _(u"discussions")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:discussion',
            kwargs={
                'project_slug': self.project.slug,
                'discussion_slug': self.slug,
            }
        )

    def save(self, *args, **kwargs):
        self.description = sanitizeHtml(self.description)
        super(SocialForumTopic, self).save(*args, **kwargs)


class SocialForumEntry(models.Model):
    """ Answers to a concrete topic, i.e. entries in the forum. """
    topic = models.ForeignKey(SocialForumTopic, verbose_name=_(u"discussion"))
    creator = models.ForeignKey(User, verbose_name=_(u"author"), related_name="social_entries")
    content = models.TextField(verbose_name=_(u"content"), default="")
    is_edited = models.BooleanField(default=False, verbose_name=_(u"edited"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_("date edited"))

    order_with_respect_to = 'topic'

    class Meta:
        ordering = ['date_created',]
        verbose_name = _(u"forum entry")
        verbose_name_plural = _(u"forum entries")

    def save(self, *args, **kwargs):
        self.content = sanitizeHtml(self.content)
        if self.pk:
            # The owner or the mod has edited the entry.
            self.is_edited = True
        super(SocialForumEntry, self).save(*args, **kwargs)

    def __str__(self):
        return u"Answer for %s" % self.topic.__unicode__()


def cleanup(sender, instance, **kwargs):
    """ Make sure that etherpad groups will be deleted along with project. """
    instance.destroy()
models.signals.post_delete.connect(cleanup, sender=SocialProject)


models.signals.post_save.connect(resize_background_image, sender=SocialProject)
models.signals.post_save.connect(project_created_action, sender=SocialProject)
models.signals.post_save.connect(project_task_action, sender=SocialForumTopic)
models.signals.post_save.connect(project_task_action, sender=SocialForumEntry)
models.signals.post_save.connect(project_task_action, sender=TaskGroup)
models.signals.post_save.connect(project_task_action, sender=Task)


@python_2_unicode_compatible
class Attachment(models.Model):
    """ Simple model holding files attached to project which visitors may download.
    """
    project = models.ForeignKey(SocialProject, related_name="attachments", verbose_name=_(u"project"))
    description = models.TextField(blank=True, default="", verbose_name=_(u"description"))
    attachment = models.FileField(upload_to='attachments/', max_length=200, verbose_name=_(u"file"))
    date_uploaded = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date uploaded"))
    uploaded_by = models.ForeignKey(User, related_name="attachments", verbose_name=_(u"user"))
    mime_type = models.CharField(max_length=255, default="")
    tasks = models.ManyToManyField(Task, null=True, blank=True, verbose_name=_(u"tasks"), related_name="attachments")

    def save(self, *args, **kwargs):
        if not self.mime_type:
            self.mime_type = mimetypes.guess_type(self.attachment.path)[0]
        super(Attachment, self).save(*args, **kwargs)

    def __str__(self):
        return self.attachment.name.split('/')[-1]


def cleanup_attachment(sender, instance, **kwargs):
    """ Make sure that files will be deleted along with attachments.
    """
    instance.attachment.delete(save=False)


models.signals.pre_delete.connect(cleanup_attachment, sender=Attachment)
