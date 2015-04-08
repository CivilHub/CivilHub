# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from slugify import slugify

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from .client import EtherpadLiteClient

# Models in this group will not work properly without server enabled.
try:
    KEY = settings.ETHERPAD_API_KEY
    URL = settings.ETHERPAD_INTERNAL_URL
except AttributeError:
    raise ImproperlyConfigured(_(u"Provide settings for Etherpad Lite Server"))


class EtherpadBaseModel(models.Model):
    """ Basic model providing etherpad server functionality. """
    @property
    def client(self):
        return EtherpadLiteClient(base_params={'apikey': KEY}, base_url=URL)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class EtherpadGroup(EtherpadBaseModel):
    """ Etherpad groups and users acts independently. """
    name = models.CharField(max_length=255)
    etherpad_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _(u"authors group")
        verbose_name_plural = _(u"authors groups")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            result = self.client.createGroupIfNotExistsFor(
                groupMapper=str(self.pk))
            self.etherpad_id = result['groupID']
        super(EtherpadGroup, self).save(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        self.client.deleteGroup(groupID=self.etherpad_id)


@python_2_unicode_compatible
class EtherpadAuthor(EtherpadBaseModel):
    """ Schema and methods for etherpad-lite authors. """
    user = models.OneToOneField(User, related_name="author")
    group = models.ManyToManyField(EtherpadGroup,
        blank=True, null=True,
        related_name="authors")
    etherpad_id = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _(u"author")
        verbose_name_plural = _(u"authors")

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.pk:
            result = self.client.createAuthorIfNotExistsFor(
                authorMapper=str(self.user.pk),
                name=self.user.get_full_name())
            self.etherpad_id = result['authorID']
        super(EtherpadAuthor, self).save(*args, **kwargs)


class Pad(EtherpadBaseModel):
    """ Basic model for single pad instance. By design pads are tied to groups. """
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=255, blank=True, default="", unique=True,
        help_text=_(u"Slug will be auto-generated if not provided"))
    group = models.ForeignKey(EtherpadGroup)

    @property
    def pad_id(self):
        return "%s$%s" % (self.group.etherpad_id, self.name.replace(' ', '_'))

    @property
    def html(self):
        response = self.client.getHTML(padID=self.pad_id)
        return response['html']

    @property
    def text(self):
        response = self.client.getText(padID=self.pad_id)
        return response['text']

    class Meta:
        verbose_name = _(u"pad")
        verbose_name_plural = _(u"pads")

    def __str__(self):
        return self.pad_id

    def get_absolute_url(self):
        if self.group.socialproject_set.count():
            project_slug = self.group.socialproject_set.first().slug
            return reverse('projects:document', kwargs={
                'project_slug': project_slug,
                'slug': self.slug,
            })
        return reverse('pad-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Provide name for Django model based on padID
        if not self.pk:
            self.client.createGroupPad(
                groupID=str(self.group.etherpad_id),
                padName=str(self.name))
        # Provide auto-generated unique slug for all pads - useful for SEO
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
                # Or shouldn't it?
                if retries >= 50:
                    raise ValidationError(u"Maximum number of retries exceeded")
                retries += 1
                self.slug = "{}-{}".format(slug, retries)
        super(Pad, self).save(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        self.client.deletePad(padID=self.pad_id)


def cleanup_etherpad(sender, instance, **kwargs):
    """ Make sure that groups and pads will be deleted in etherpad-lite db. """
    instance.destroy()
models.signals.pre_delete.connect(cleanup_etherpad, sender=EtherpadGroup)
models.signals.pre_delete.connect(cleanup_etherpad, sender=Pad)


def activate_user_author(sender, instance, **kwargs):
    """ Creates new ehterpad author instnce when user register. """
    try:
        author = EtherpadAuthor.objects.get(user=instance)
    except EtherpadAuthor.DoesNotExist:
        author = EtherpadAuthor.objects.create(user=instance)
    return author
models.signals.post_save.connect(activate_user_author, sender=User)
