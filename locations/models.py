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
# Override system storage: 
#http://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file
from places_core.storage import OverwriteStorage, ReplaceStorage
from places_core.helpers import sanitizeHtml, sort_by_locale
from gallery.image_manager import ImageManager as IM
from gallery.image import resize_background_image, delete_background_image, \
                           delete_image, rename_background_file

from .signals import update_parent_cache, adjust_created_location


def get_upload_path(instance, filename):
    return 'img/locations/' + uuid4().hex + os.path.splitext(filename)[1]


def obj_to_dict(obj):
    """
    Helper który zamienia nam rózne typy zawartości na zunifikowany format, co
    ułatwi nam wyświetlanie ich w templatach. Działa jak prosty serializer.
    """
    content_type = ContentType.objects.get_for_model(obj)

    context = {
        'type': content_type.model,
        'name': capfirst(_(content_type.model)),
        'slug': obj.slug,
        'ct'  : content_type.pk,
        'pk'  : obj.pk,
        'url' : obj.get_absolute_url(),
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

    if hasattr(obj, 'category') and obj.category is not None and obj.category.pk:
        context.update({'category': {
            'pk': obj.category.pk,
            'name': obj.category.__unicode__(),
        }})

    if hasattr(obj, 'retina_thumbnail') and not obj.has_default_image:
        context['retina_thumbnail'] = obj.retina_thumbnail

    if content_type.model == 'idea':
        context.update({
            'description': obj.description,
            'meta': {'votes': obj.get_votes(),}
        })

    elif content_type.model == 'poll':
        context.update({'description': obj.question})

    elif content_type.model == 'news':
        context.update({'description': obj.content})

    elif content_type.model == 'discussion':
        context.update({
            'description': obj.intro,
            'meta': {
                'answers': obj.entry_set.count(),
            }
        })

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


class LocationLocaleManager(models.Manager):
    """
    Manager umożliwiający porządkowanie lokalizacji alfabetycznie z uwzględnieniem
    lokalnych znaków utf-8.
    """
    def get_queryset(self):
        return sort_by_locale(super(LocationLocaleManager, self).get_queryset(),
                                lambda x: x.__unicode__(), get_language())


class BackgroundModelMixin(object):
    """ Mixin dla modeli obsługujących obraz tła. """
    def get_image_url(self, size=(1920,300), retina=False):

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
        return self.get_image_url((270,190))

    def background_url(self):
        return self.get_image_url()

    def retina_background_url(self):
        return self.get_image_url(retina=True)



@python_2_unicode_compatible
class Location(models.Model, BackgroundModelMixin):
    """ Basic location model. """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=10000, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    names = models.ManyToManyField(AlterLocationName, blank=True, null=True, related_name='alternames')
    creator = models.ForeignKey(User, blank=True, related_name='created_locations')
    users = models.ManyToManyField(User, blank=True)
    parent = models.ForeignKey('Location', blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=10)
    image = models.ImageField(upload_to=get_upload_path, default='img/locations/nowhere.jpg')
    # Tutaj oznaczamy regiony/miasta/stolice itp. oznaczeniami z geonames
    kind = models.CharField(max_length=10)

    # custom managers
    objects = models.Manager()
    locale_sorted = LocationLocaleManager()

    class Meta:
        ordering = ['name',]
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
        # Generujemy odpowiedni slug
        if not self.slug:
            slug_entry = slugify('-'.join([self.name, self.country_code]))
            chk = Location.objects.filter(slug__icontains=slug_entry).count()
            if chk:
                slug_entry = slug_entry + '-' + str(chk)
            self.slug = slug_entry
        # Sprawdzamy, czy zmienił się obrazek i w razie potrzeby usuwamy stary
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
                    'pk'  : self.parent.pk,
                    'name': self.parent.__unicode__(),
                    'url' : self.parent.get_absolute_url(),
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
                ancestors.append({
                    'name': a.__unicode__(),
                    'url' : a.get_absolute_url(),
                })
            else:
                ancestors.append(a)
            if a.location_set.count() > 0:
                a.get_ancestor_chain(ancestors, response)
        return ancestors

    def get_children_id_list(self, ids=None):
        """ Returns all id's of sublocations for this location. """
        if ids == None: ids = []
        for a in self.location_set.all():
            ids.append(a.pk)
            if a.location_set.count() > 0:
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
            tmp.append({
                'user' : user,
                'count': self.count_users_actions(user),
            })
        tmp = sorted(tmp, key=operator.itemgetter('count'))
        actions = reversed(tmp)

        return actions

    def get_absolute_url(self):
        return reverse('locations:details', kwargs={'slug':self.slug})

    def get_description(self):
        return self.description

    def get_cropped_image(self):
        """ Method to get cropped background for list views. """
        return rename_background_file(self.image.url)

    def content_objects(self):
        """ Zwraca listę obiektów powiązanych z tą lokalizacją (idee, dyskusje,
        newsy i ankiety), sortowane od najnowszych. """
        qs = [obj_to_dict(x) for x in self.poll_set.all()]
        qs += [obj_to_dict(x) for x in self.news_set.all()]
        qs += [obj_to_dict(x) for x in self.idea_set.all()]
        qs += [obj_to_dict(x) for x in self.discussion_set.all()]
        return sorted(qs, key=lambda x: x['date_created'], reverse=True)

    def __str__(self):
        lang = get_language().split('-')[0]
        alt = self.names.filter(language=lang)
        if not len(alt):
            return self.name
        else:
            return alt[0].altername


@python_2_unicode_compatible
class Country(models.Model):
    """ """
    code = models.CharField(max_length=2)
    location = models.OneToOneField(Location, related_name='country')

    class Meta:
        ordering = ['code',]

    def get_capital(self):
        try:
            return Location.objects.get(country_code=self.code, kind="PPLC")
        except Location.DoesNotExist:
            return None

    def __str__(self):
        return self.code


from maps.signals import create_marker
post_delete.connect(delete_background_image, sender=Location)
post_save.connect(resize_background_image, sender=Location)
post_save.connect(adjust_created_location, sender=Location)
post_save.connect(create_marker, sender=Location)
post_save.connect(update_parent_cache, sender=Location)
