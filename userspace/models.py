# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from slugify import slugify
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.core.urlresolvers import reverse, NoReverseMatch
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
from locations.models import Location, BackgroundModelMixin
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
class UserProfile(models.Model, BackgroundModelMixin):
    """ User profile. """
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    lang = models.CharField(
        max_length = 7,
        choices = settings.LANGUAGES,
        default = settings.LANGUAGE_CODE,
        verbose_name = _(u"language")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_(u"about"))
    rank_pts  = models.IntegerField(blank=True, default=0, verbose_name=_(u"points"))
    birth_date = models.CharField(max_length=20, blank=True, null=True, verbose_name=_(u"birth date"))
    mod_areas = models.ManyToManyField(Location, related_name='locations', blank=True)
    clean_username = models.SlugField(blank=True, null=True, max_length=255)
    website = models.URLField(max_length=255, blank=True, null=True, verbose_name=_(u"website"))
    gender = models.CharField(
        max_length=1,
        choices = (('M', _('male')),('F', _('female')),('U', _('undefined'))),
        blank=True,
        null=True,
        verbose_name=_(u"gender")
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
        default = 'img/avatars/anonymous.jpg',
        storage = OverwriteStorage()
    )
    thumbnail = models.ImageField(
        upload_to = "img/avatars/",
        default = 'img/avatars/30x30_anonymous.jpg',
        storage = OverwriteStorage()
    )
    image = models.ImageField(
        upload_to = get_upload_path,
        default = 'img/backgrounds/background.jpg'
    )

    @property
    def has_default_avatar(self):
        """ Check if user personally changed avatar picture. """
        return u'anonymous' in self.avatar.name

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
                if not u'background.jpg' in orig.image.name and orig.image != self.image:
                    delete_image(orig.image.path)
                    delete_image(rename_background_file(orig.image.path))
            except UserProfile.DoesNotExist:
                pass
        super(UserProfile, self).save(*args, **kwargs)

    def set_default_avatar(self):
        self.avatar = 'img/avatars/anonymous.jpg'
        self.thumbnail = 'img/avatars/30x30_anonymous.jpg'
        self.save()

    def set_default_background(self):
        self.image = 'img/backgrounds/background.jpg'
        self.save()

    def thumbnail_small(self):
        return thumbnail(self.avatar.name, 30)

    def thumbnail_medium(self):
        return thumbnail(self.avatar.name, 60)

    def thumbnail_big(self):
        return thumbnail(self.avatar.name, 100)

    def get_biggest_locations(self, limit=5):
        """
        This function returns a list of the greatest location that user subscribes.
        Parameter specifies the length of the list 'limit'.
        """
        my_locations = self.user.location_set.all()
        return my_locations.order_by('users')[:limit]

    def followed_locations(self):
        """ The method returns a list of locations follows by the user. """
        follows = [x for x in following(self.user, Location) if x is not None]
        return sort_by_locale(follows, lambda x: x.name, get_language())

    def followed_users(self):
        return [x for x in following(self.user, User) if x is not None]

    def followers(self):
        return followers(self.user)

    def get_cropped_image(self):
        """ Method to get cropped background for list views. """
        return rename_background_file(self.image.url)

    def get_absolute_url(self):
        try:
            url = reverse('user:profile', kwargs={'username': self.clean_username})
        except NoReverseMatch:
            clean_username = slugify(self.user.get_full_name())
            chk = UserProfile.objects.filter(clean_username=clean_username).count()
            if chk:
                self.clean_username = "%s-%d" % (clean_username, self.pk)
            else:
                self.clean_username = clean_username
            url = reverse('user:profile', kwargs={'username': self.clean_username})
        return url

    def __str__(self):
        return self.user.get_full_name()


@python_2_unicode_compatible
class Badge(models.Model):
    """
    Badges for users for achievements - eg. The application of ideas, which
    has been accepted and implemented, etc., etc.
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
    Model that stores user data indicating their willingness to registration
    before the account is activated.
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


@python_2_unicode_compatible
class CloseAccountDemand(models.Model):
    """ Similar to register demand, this model holds info about that some user
        wants to close his/her account. This way we have time to change his mind.
        After this period user account will be not removed from database but
        rather set to inactive and his email address should be removed.
    """
    user = models.ForeignKey(User, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def deactivate(self):
        self.user.is_active = False
        self.user.email = ""
        self.user.save()
        self.is_deleted = True
        self.save()

    def __str__(self):
        return u"<Delete account demand for {}>".format(self.user.email)

    class Meta:
        verbose_name = _(u"close account demand")
        verbose_name_plural = _(u"close account demands")


class LoginData(models.Model):
    """
    Table storing login information, including user name, IP address and login date.
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    address = models.IPAddressField()

    class Meta:
        ordering = ['-date',]

    def save(self, *args, **kwargs):
        """ Ensure maximum number of entries per user in db. """
        super(LoginData, self).save(*args, **kwargs)
        max_entries = 5
        if hasattr(settings, 'MAX_LOGIN_ENTRIES'):
            max_entries = settings.MAX_LOGIN_ENTRIES
        prx_entries = LoginData.objects.filter(user=self.user)
        if len(prx_entries) > max_entries:
            for i in range(1, len(prx_entries) - max_entries + 1):
                LoginData.objects.last().delete()


def activate_user_profile(sender, instance, **kwargs):
    """ Creates new user profile when user register. """
    try:
        profile = UserProfile.objects.get(user=instance)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=instance)
    return profile


post_delete.connect(delete_background_image, sender=UserProfile)
post_save.connect(resize_background_image, sender=UserProfile)
post_save.connect(activate_user_profile, sender=User)
