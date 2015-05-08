# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator, os, json
from uuid import uuid4
from slugify import slugify

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.template.defaultfilters import capfirst, truncatewords_html
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from actstream.models import model_stream
from places_core.helpers import sanitizeHtml
from places_core.storage import OverwriteStorage, ReplaceStorage
from gallery.image_manager import ImageManager as IM
from gallery.image import resize_background_image, delete_background_image, \
                           delete_image, rename_background_file

from .managers import LocationLocaleManager


def get_upload_path(instance, filename):
    return 'img/locations/' + uuid4().hex + os.path.splitext(filename)[1]


def obj_to_dict(obj):
    """
    A helper that changes various types of content into a unified format,
    that will help us show them in templates. Works as a simple serializer.
    *deprecated* - it's much better to use activities app.
    """
    content_type = ContentType.objects.get_for_model(obj)

    context = {
        'type': content_type.model,
        'name': capfirst(_(content_type.model)),
        'slug': obj.slug,
        'ct': content_type.pk,
        'pk': obj.pk,
        'url': obj.get_absolute_url(),
        'title': obj.__unicode__(),
        'image': obj.image_url,
        'thumbnail': obj.thumbnail,
        'retina_thumbnail': False,
        'location': obj.location.__unicode__(),
        'meta': {},
        'date_created': obj.date_created.isoformat(),
        'creator': {
            'id': obj.creator.pk,
            'url': obj.creator.profile.get_absolute_url(),
            'img': obj.creator.profile.avatar.url,
            'name': obj.creator.get_full_name(),
        },
    }

    if hasattr(obj,
               'category') and obj.category is not None and obj.category.pk:
        context.update({
            'category':
            {'pk': obj.category.pk,
             'name': obj.category.__unicode__(), }
        })

    if hasattr(obj, 'retina_thumbnail') and not obj.has_default_image:
        context['retina_thumbnail'] = obj.retina_thumbnail

    if hasattr(obj, 'has_default_image'):
        context['default_image'] = obj.has_default_image

    if content_type.model == 'idea':
        context.update({
            'description': obj.description,
            'meta': {'votes': obj.get_votes(), }
        })

    elif content_type.model == 'poll':
        context.update({'description': obj.question})

    elif content_type.model == 'news':
        context.update({'description': obj.content})

    elif content_type.model == 'discussion':
        context.update({
            'description': obj.intro,
            'meta': {'answers': obj.entry_set.count(), }
        })

    elif content_type.model == 'socialproject':
        context['description'] = obj.get_description()
        context['name'] = _(u"Project")

    else:
        raise Exception(_(u"Wrong model instance"))
    context['description'] = truncatewords_html(context['description'], 15)
    return context


class AlterLocationName(models.Model):
    """ Simple model to hold location name translations. """
    altername = models.CharField(max_length=200)
    language = models.CharField(max_length=2)

    def __unicode__(self):
        return self.altername


class BackgroundModelMixin(object):
    """ A mixin for models that take care of the background image."""

    def get_image_url(self, size=(1920, 300), retina=False):

        # Get first part of image url
        url = self.image.url.split('/')
        url.pop()
        url = '/'.join(url)

        # Rename files using gallery manager
        # FIXME: this behavior should be bound to ImageManager
        try:
            im = IM(self.image.path)
        except Exception:
            return self.image.url

        if retina:
            suffix = "{}x{}@2x".format(size[0], size[1])
            filename = im.create_filename(suffix=suffix).split('/')[-1]
        else:
            suffix = "{}x{}".format(size[0], size[1])
            filename = im.create_filename(suffix=suffix).split('/')[-1]
        return u"{}/{}".format(url, filename)

    def thumb_url(self, retina=False):
        return self.get_image_url((270, 190))

    def background_url(self):
        return self.get_image_url()

    def retina_background_url(self):
        return self.get_image_url(retina=True)


@python_2_unicode_compatible
class Location(models.Model, BackgroundModelMixin):
    """ Basic location model. """
    name = models.CharField(max_length=200, verbose_name=_(u"name"))
    slug = models.SlugField(max_length=200,
                            unique=True,
                            verbose_name=_(u"slug"))
    description = models.TextField(max_length=10000,
                                   blank=True,
                                   verbose_name=_(u"description"))
    latitude = models.FloatField(blank=True,
                                 null=True,
                                 verbose_name=_(u"latitude"))
    longitude = models.FloatField(blank=True,
                                  null=True,
                                  verbose_name=_(u"longitude"))
    names = models.ManyToManyField(AlterLocationName,
                                   blank=True,
                                   null=True,
                                   related_name='alternames',
                                   verbose_name=_(u"alternate names"))
    creator = models.ForeignKey(User,
                                blank=True,
                                related_name='created_locations',
                                verbose_name=_(u"creator"))
    users = models.ManyToManyField(User, blank=True, verbose_name=_(u"users"))
    parent = models.ForeignKey('Location',
                               blank=True,
                               null=True,
                               verbose_name=_(u"parent"))
    population = models.IntegerField(blank=True,
                                     null=True,
                                     verbose_name=_(u"population"))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_(u"date created"))
    country_code = models.CharField(max_length=10,
                                    verbose_name=_(u"country code"))
    image = models.ImageField(upload_to=get_upload_path,
                              default='img/locations/nowhere.jpg',
                              verbose_name=_(u"image"))
    # Hold entire parent chain for faster searching (hopefully)
    parent_list = models.CharField(
        max_length=255,
        verbose_name=_(u"parent list"),
        blank=True,
        null=True,
        help_text=_(u"List of parent location ID's separated with comma"))
    # Hold 1-st level children list
    children_list = models.CharField(
        max_length=255,
        verbose_name=_(u"children list"),
        blank=True,
        null=True,
        help_text=_(u"List of children ID's separated with comma"))
    # Here we mark regions/cities/capitals etc. with geonames
    kind = models.CharField(max_length=10, verbose_name=_(u"kind"))

    # custom managers
    objects = models.Manager()
    locale_sorted = LocationLocaleManager()

    #contents = LocationContentManager

    class Meta:
        ordering = ['name', ]
        verbose_name = _(u"location")
        verbose_name_plural = _(u"locations")

    def country_name(self):
        """ Get location's country name. """
        try:
            country = Country.objects.get(code=self.country_code)
            return country.location.__unicode__()
        except Country.DoesNotExist:
            return _("Unknown")

    def count_objects(self, content_types=None):
        """
        Count all objects related to this location (sublocations and content).
        """
        subs = self.get_children_id_list()
        count = len(subs)
        for s in subs:
            l = Location.objects.get(pk=s)
            count += l.idea_set.count()
            count += l.discussion_set.count()
            count += l.poll_set.count()
            count += l.news_set.count()
        return count

    def save(self, *args, **kwargs):
        self.description = sanitizeHtml(self.description)
        if self.parent is not None:
            self.country_code = self.parent.country_code
        self.parent_list = ",".join([str(x)
                                     for x in self.get_parent_id_list()])
        # We generate the appropriate slug
        if not self.slug:
            slug_entry = slugify('-'.join([self.name, self.country_code]))
            chk = Location.objects.filter(slug__icontains=slug_entry).count()
            if chk:
                slug_entry = slug_entry + '-' + str(chk)
            self.slug = slug_entry
        # We check whether the image has changed and if needed, we delete the old one
        # FIXME: we are using signal for now, this is no longer necessary and deprecated.
        try:
            orig = Location.objects.get(pk=self.pk)
            if not u'nowhere' in orig.image.name and orig.image != self.image:
                delete_image(orig.image.path)
                delete_image(rename_background_file(orig.image.path))
        except Location.DoesNotExist:
            pass
        super(Location, self).save(*args, **kwargs)

    def get_parent_chain(self, parents=None, response='JSON'):
        """
        Take all parent location in 'chain' of name - url pairs. `response` is
        faked parameter made because of backwards compatibility. If provided
        as 'QUERYSET', function will return Django queryset, not dictionary.
        """
        if parents == None:
            parents = []
        if self.parent:
            if response == 'JSON':
                parents.append({
                    'pk': self.parent.pk,
                    'name': self.parent.__unicode__(),
                    'url': self.parent.get_absolute_url(),
                })
            else:
                parents.append(self.parent)
            if self.parent.parent:
                self.parent.get_parent_chain(parents, response)
        return reversed(parents)

    def get_ancestor_chain(self, ancestors=None, response='JSON'):
        """
        Get all sublocations and return dictionary of name - url pairs. The
        reason of `response` argument is the same as in get_parent_chain
        method.
        """
        if ancestors == None:
            ancestors = []
        for a in self.location_set.all():
            if response == 'JSON':
                ancestors.append(
                    {'name': a.__unicode__(),
                     'url': a.get_absolute_url(), })
            else:
                ancestors.append(a)
            if a.location_set.count() > 0:
                a.get_ancestor_chain(ancestors, response)
        return ancestors

    def get_parent_id_list(self, ids=None):
        if ids is None:
            ids = []
        if self.parent is not None:
            ids.append(self.parent.pk)
            self.parent.get_parent_id_list(ids)
        return ids

    @property
    def get_parents(self):
        if self.parent_list is None:
            return []
        return [int(x) for x in self.parent_list.split(',') if x]

    def get_children_id_list(self, ids=None):
        """ Returns all id's of sublocations for this location. """
        if ids is None:
            ids = []
        for a in self.location_set.all():
            ids.append(a.pk)
            a.get_children_id_list(ids)
        return ids

    def count_users_actions(self, user):
        """
        Count actions related to this place performed
        by particular provided user.
        """
        ct = ContentType.objects.get_for_model(User)
        pk = user.pk
        target_ct = ContentType.objects.get_for_model(self)
        stream = model_stream(self)
        actions = stream.filter(target_content_type=target_ct)
        actions = actions.filter(actor_content_type=ct)
        actions = actions.filter(actor_object_id=pk)
        actions = actions.filter(target_object_id=self.pk)
        return actions.count()

    def most_active_followers(self, limit=10):
        """ Show the most active followers of current place. """
        tmp = []
        for user in self.users.all():
            tmp.append(
                {'user': user,
                 'count': self.count_users_actions(user), })
        tmp = sorted(tmp, key=operator.itemgetter('count'))
        actions = reversed(tmp)

        return actions

    def get_absolute_url(self):
        return reverse('locations:details', kwargs={'slug': self.slug})

    def get_description(self):
        return self.description

    def get_cropped_image(self):
        """ Method to get cropped background for list views. """
        return rename_background_file(self.image.url)

    def content_objects(self):
        """ Returns a list of objects connected with this location (idea, discussion,
        news and poll), sorts from latest. """
        qs = [obj_to_dict(x) for x in self.poll_set.all()]
        qs += [obj_to_dict(x) for x in self.news_set.all()]
        qs += [obj_to_dict(x) for x in self.idea_set.all()]
        qs += [obj_to_dict(x) for x in self.discussion_set.all()]
        qs += [obj_to_dict(x) for x in self.projects.all()]
        return sorted(qs, key=lambda x: x['date_created'], reverse=True)

    def published_items(self, content_type=None):
        """
        Returns list of content item ID's grouped by content type.
        Very useful for content management and activity stream relation.
        TODO: select content type/content types to choose from.
        FIXME: this is REALLY ugly...
        """
        idea_key = ContentType.objects.get(app_label='ideas', model='idea').pk
        poll_key = ContentType.objects.get(app_label='polls', model='poll').pk
        discussion_key = ContentType.objects.get(app_label='topics', model='discussion').pk
        project_key = ContentType.objects.get(app_label='projects', model='socialproject').pk
        gallery_key = ContentType.objects.get(app_label='gallery', model='locationgalleryitem').pk
        blog_key = ContentType.objects.get(app_label='blog', model='news').pk

        items = {}
        items[idea_key] = [x[0] for x in self.idea_set.values_list('pk')]
        items[poll_key] = [x[0] for x in self.poll_set.values_list('pk')]
        items[discussion_key] = [x[0] for x in self.discussion_set.values_list('pk')]
        items[gallery_key] = [x[0] for x in self.pictures.values_list('pk')]
        items[blog_key] = [x[0] for x in self.news_set.values_list('pk')]

        for l in self.location_set.all():
            items[idea_key] = items[idea_key] + [x[0] for x in l.idea_set.values_list('pk')]
            items[poll_key] = items[poll_key] + [x[0] for x in l.poll_set.values_list('pk')]
            items[discussion_key] = items[discussion_key] + [x[0] for x in l.discussion_set.values_list('pk')]
            items[gallery_key] = items[gallery_key] + [x[0] for x in l.pictures.values_list('pk')]
            items[blog_key] = items[blog_key] + [x[0] for x in l.news_set.values_list('pk')]

        return items

    def __str__(self):
        lang = get_language().split('-')[0]
        alt = self.names.filter(language=lang)
        if not len(alt):
            return self.name
        else:
            return alt[0].altername


post_save.connect(resize_background_image, sender=Location)


@python_2_unicode_compatible
class Country(models.Model):
    """ """
    code = models.CharField(max_length=2)
    location = models.OneToOneField(Location, related_name='country')

    class Meta:
        ordering = ['code', ]

    def get_capital(self):
        try:
            return Location.objects.get(country_code=self.code, kind="PPLC")
        except Location.DoesNotExist:
            return None

    def __str__(self):
        return self.code
