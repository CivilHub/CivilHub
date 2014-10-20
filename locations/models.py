# -*- coding: utf-8 -*-
import operator, os, json
from uuid import uuid4
from slugify import slugify
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import get_language
from actstream.models import model_stream
# Override system storage: 
#http://stackoverflow.com/questions/9522759/imagefield-overwrite-image-file
from places_core.storage import OverwriteStorage, ReplaceStorage
from places_core.helpers import sanitizeHtml, sort_by_locale
from gallery.image import resize_background_image, delete_background_image, \
                           delete_image, rename_background_file


def get_country_codes():
    """
    Funkcja, która odczytuje plik .json przechowujący kody państ przyporząd-
    kowane do ich nazw i zwraca je w postaci listy.
    """
    f = open(os.path.join(settings.BASE_DIR, 'geobase/data/codes.json'))
    data = json.loads(f.read())
    f.close()
    codes = []
    for row in data:
        codes.append((row['code'], row['name']))
    return codes


def get_upload_path(instance, filename):
    return 'img/locations/' + uuid4().hex + os.path.splitext(filename)[1]


class LocationLocaleManager(models.Manager):
    """
    Manager umożliwiający porządkowanie lokalizacji alfabetycznie z uwzględnieniem
    lokalnych znaków utf-8.
    """
    def get_queryset(self):
        return sort_by_locale(super(LocationLocaleManager, self).get_queryset(),
                                lambda x: x.name, get_language())


class Location(models.Model):
    """ Basic location model. """
    OBJ_TYPES = (
        ('country', 'Country'),
        ('region', 'Region'),
        ('subregion', 'Subregion'),
        ('district', 'District'),
        ('city', 'City')
    )
    
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique=True)
    # Helps with relation to django-cities models
    geo_type = models.CharField(max_length=24, choices=OBJ_TYPES, default='city')
    description = models.TextField(max_length=10000, blank=True)
    latitude  = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    creator   = models.ForeignKey(User, blank=True, related_name='created_locations')
    users     = models.ManyToManyField(User, blank=True)
    parent    = models.ForeignKey('Location', blank=True, null=True)
    population= models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    country_code = models.CharField(max_length=2,
                                    choices=get_country_codes())
    image     = models.ImageField(
        upload_to = get_upload_path,
        default = 'img/locations/nowhere.jpg'
    )
    
    objects = models.Manager()
    locale_sorted = LocationLocaleManager()
    
    class Meta:
        ordering = ['name',]

    def save(self, *args, **kwargs):
        self.description = sanitizeHtml(self.description)
        # Generujemy odpowiedni slug
        if not self.slug:
            to_slug_entry = slugify('-'.join([self.name, self.country_code]))
            chk = Location.objects.filter(slug=to_slug_entry)
            if len(chk) > 0:
                mod = len(chk)
                to_slug_entry = to_slug_entry + '-' + str(mod)
                while Location.objects.filter(slug=to_slug_entry).count():
                    mod += 1
                    to_slug_entry = to_slug_entry + '-' + str(mod)
            self.slug = slugify(to_slug_entry)
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
                    'name': self.parent.name,
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
                    'name': a.name,
                    'url' : a.get_absolute_url(),
                })
            else:
                ancestors.append(a)
            if a.location_set.count() > 0:
                a.get_ancestor_chain(ancestors, response)
        return ancestors

    def get_children_id_list(self, ids=None):
        """ Returns all sublocations for this location. """
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

    def __unicode__(self):
        return self.name


from maps.signals import create_marker
post_delete.connect(delete_background_image, sender=Location)
post_save.connect(resize_background_image, sender=Location)
post_save.connect(create_marker, sender=Location)
