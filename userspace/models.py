# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from slugify import slugify
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from actstream.models import following, followers

from places_core.storage import OverwriteStorage, ReplaceStorage
from places_core.helpers import sort_by_locale
from locations.models import Location
from gallery.image import resize_background_image, delete_background_image, \
                           delete_image, rename_background_file


def thumbnail(imgname, size):
    """
    Returns profile avatar in selected size. It takes full path to profile
    image (e.g profile.avatar.name) and selected size which should be integer
    meaning thumb width.
    """
    file, ext = os.path.splitext(imgname.split('/')[-1:][0])
    pathname = os.path.join(settings.MEDIA_URL, '/'.join(imgname.split('/')[:-1]))
    return pathname + '/' + str(size) + 'x' + str(size) + '_' + file + ext


def get_upload_path(instance, filename):
    return 'img/backgrounds/' + uuid4().hex + os.path.splitext(filename)[1]


@python_2_unicode_compatible
class UserProfile(models.Model):
    """
    Profil użytkownika.
    """
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    lang = models.CharField(
        max_length = 7,
        choices = settings.LANGUAGES,
        default = settings.LANGUAGE_CODE
    )
    description = models.TextField(blank=True, null=True)
    rank_pts  = models.IntegerField(blank=True, default=0)
    birth_date = models.CharField(max_length=20, blank=True, null=True)
    mod_areas = models.ManyToManyField(Location, related_name='locations', blank=True)
    clean_username = models.SlugField(blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices = (('M', _('male')),('F', _('female')),('U', _('undefined'))),
        blank=True,
        null=True
    )
    gplus_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Google+ profile url")
    )
    fb_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name = _("Facebook profile url")
    )
    twt_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name = _("Twitter profile url")
    )
    linkedin_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name = _("LinkedIn profile url")
    )
    avatar = models.ImageField(
        upload_to = "img/avatars/",
        default = 'img/avatars/anonymous.png',
        storage = OverwriteStorage()
    )
    thumbnail = models.ImageField(
        upload_to = "img/avatars/",
        default = 'img/avatars/30x30_anonymous.png',
        storage = OverwriteStorage()
    )
    background_image = models.ImageField(
        upload_to = get_upload_path,
        default = 'img/backgrounds/background.jpg'
    )

    def save(self, *args, **kwargs):
        if self.description:
            self.description = strip_tags(self.description)
        if not self.clean_username:
            clean_username = slugify(self.user.get_full_name())
            chk = UserProfile.objects.filter(clean_username=clean_username).count()
            if chk:
                self.clean_username = "%s-%d" % (clean_username, self.pk)
            else:
                self.clean_username = clean_username
        # Sprawdzamy, czy zmienił się obrazek i w razie potrzeby usuwamy stary
        if self.pk:
            try:
                orig = UserProfile.objects.get(pk=self.pk)
                if not u'background.jpg' in orig.background_image.name and orig.background_image != self.background_image:
                    delete_image(orig.background_image.path)
                    delete_image(rename_background_file(orig.background_image.path))
            except UserProfile.DoesNotExist:
                pass
        super(UserProfile, self).save(*args, **kwargs)

    def thumbnail_small(self):
        return thumbnail(self.avatar.name, 30)
        
    def thumbnail_medium(self):
        return thumbnail(self.avatar.name, 60)

    def thumbnail_big(self):
        return thumbnail(self.avatar.name, 90)

    def get_biggest_locations(self, limit=5):
        """
        Funkcja zwraca listę największych lokalizacji, jakie subskrybuje
        użytkownik. Długość listy określa parametr 'limit'.
        """
        my_locations = self.user.location_set.all()
        return my_locations.order_by('users')[:limit]

    def followed_locations(self):
        """ Metoda zwraca listę lokalizacji obserwowanych przez użytkownika. """
        return sort_by_locale(following(self.user, Location), lambda x: x.name, get_language())

    def followers(self):
        return followers(self.user)

    def get_cropped_image(self):
        """ Method to get cropped background for list views. """
        return rename_background_file(self.background_image.url)

    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'username': self.clean_username})

    def __str__(self):
        return self.user.get_full_name()


@python_2_unicode_compatible
class Badge(models.Model):
    """
    Odznaki dla użytkowników za osiągnięcia - np. zgłoszenie idei, która
    została zaakceptowana i zrealizowana itp. itd.
    """
    name = models.CharField(max_length=128)
    description = models.TextField()
    user = models.ManyToManyField(
        UserProfile,
        related_name='badges',
        blank=True
    )
    thumbnail = models.ImageField(
        upload_to = "img/badges",
        default = "img/badges/badge.png",
        storage = OverwriteStorage()
    )

    def __str__(self):
        return self.name


class RegisterDemand(models.Model):
    """
    Model przechowujący dane użytkowników zgłaszających chęć rejestracji
    zanim konto zostanie aktywowane.
    """
    activation_link = models.CharField(max_length=1024)
    ip_address    = models.IPAddressField()
    email = models.EmailField(max_length=256)
    lang = models.CharField(max_length=10, default=settings.LANGUAGE_CODE)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        primary_key=True,
        related_name='registration'
    )


class LoginData(models.Model):
    """
    Tabela przechowująca dane logowania włącznie z nazwą użytkownika,
    adresem IP oraz datą logowania.
    TODO: Przechowywanie tylko 5 ostatnich sesji.
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    address = models.IPAddressField()


post_delete.connect(delete_background_image, sender=UserProfile)
post_save.connect(resize_background_image, sender=UserProfile)
