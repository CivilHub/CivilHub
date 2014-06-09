# -*- coding: utf-8 -*-
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from places_core.storage import OverwriteStorage
from locations.models import Location


class UserProfile(models.Model):
    """
    Profil użytkownika.
    """
    user = AutoOneToOneField(User, primary_key=True, related_name='profile')
    description = models.TextField(blank=True, null=True)
    birth_date  = models.CharField(max_length=10, blank=True)
    rank_pts  = models.IntegerField(blank=True, default=0)
    mod_areas = models.ManyToManyField(Location, related_name='locations', blank=True)
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

    def get_biggest_locations(self, limit=5):
        """
        Funkcja zwraca listę największych lokalizacji, jakie subskrybuje
        użytkownik. Długość listy określa parametr 'limit'.
        """
        my_locations = self.user.location_set.all()
        return my_locations.order_by('users')[:limit]

    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'username': self.user.username})

    def __unicode__(self):
        return self.user.get_full_name()


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

    def __unicode__(self):
        return self.name


class RegisterDemand(models.Model):
    """
    Model przechowujący dane użytkowników zgłaszających chęć rejestracji
    zanim konto zostanie aktywowane.
    TODO: to trzeba później połączyć z cronem i wywalać żądania starsze niż
    określona data.
    """
    activation_link = models.CharField(max_length=1024)
    ip_address = models.IPAddressField()
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
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    address = models.IPAddressField()
