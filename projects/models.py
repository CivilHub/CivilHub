# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slugify import slugify

from django.db import models
from django.utils.html import strip_tags
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from ordered_model.models import OrderedModel

from places_core.helpers import sanitizeHtml
from locations.models import Location, BackgroundModelMixin
from userspace.models import UserProfile

from .signals import project_created_action, project_task_action


def get_upload_path(instance, filename):
    """ Ustawia ścieżkę i losową nazwę dla obrazu. """
    return 'img/projects/' + uuid4().hex + os.path.splitext(filename)[1]


@python_2_unicode_compatible
class SocialProject(BackgroundModelMixin, models.Model):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    slug = models.CharField(max_length=210, verbose_name=(u"slug"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    location = models.ForeignKey(Location, verbose_name=_(u"location"), related_name="projects")
    participants = models.ManyToManyField(UserProfile, verbose_name=_(u"participants"), blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_(u"date created"))
    date_changed = models.DateTimeField(auto_now=True, verbose_name=_(u"date changed"))
    is_done = models.BooleanField(default=False, verbose_name=_(u"finished"))
    creator = models.ForeignKey(UserProfile, verbose_name=_(u"created by"), related_name="projects")
    image = models.ImageField(blank=True, upload_to=get_upload_path, default='img/projects/default.jpg')

    class Meta:
        verbose_name = _(u"project")
        verbose_name_plural = _(u"projects")

    @property
    def progress(self):
        """
        Zwraca przybliżoną wartość procentową "zaawansowania" projektu. Sposób
        obliczania jest bardzo prosty, wyliczamy średnią ukończonych zadań.
        """
        all_tasks = sum([group.task_set.count() for group in self.taskgroup_set.all()])
        finished_tasks = sum([group.task_set.filter(is_done=True).count()\
                              for group in self.taskgroup_set.all()])
        if not finished_tasks:
            return 0
        return int(float(finished_tasks) / float(all_tasks) * 100)

    def get_description(self):
        return self.description

    def get_absolute_url(self):
        return reverse('locations:project_details', kwargs={
            'location_slug': self.location.slug,
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        """
        Provides 'clean' slug for this object, adding number of such elements
        to base name. Additionaly, we sanitize input from user.
        """
        self.name = strip_tags(self.name)
        self.description = sanitizeHtml(self.description)
        slug = slugify(self.name)
        if not self.slug:
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
        super(SocialProject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TaskGroup(OrderedModel):
    """ """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    description = models.TextField(blank=True, default='', verbose_name=_(u"description"))
    project = models.ForeignKey(SocialProject, verbose_name=_(u"project"))
    creator = models.ForeignKey(UserProfile, verbose_name=_(u"created by"), related_name="task_groups")

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
    participants = models.ManyToManyField(UserProfile, verbose_name=_(u"participants"), blank=True, null=True)
    is_done = models.BooleanField(default=False, verbose_name=_(u"finished"))
    creator = models.ForeignKey(UserProfile, verbose_name=_(u"created by"), related_name="tasks")

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


models.signals.post_save.connect(project_created_action, sender=SocialProject)
models.signals.post_save.connect(project_task_action, sender=TaskGroup)
models.signals.post_save.connect(project_task_action, sender=Task)
