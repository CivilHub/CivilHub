# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class GeoName(models.Model):
    """ Basic model for geoname instances. """
    name = models.CharField(max_length=200)
    name_std = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    feature_class = models.CharField(max_length=200)
    feature_code = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    admin1 = models.CharField(max_length=200, null=True, blank=True)
    admin2 = models.CharField(max_length=200, null=True, blank=True)
    admin3 = models.CharField(max_length=200, null=True, blank=True)
    admin4 = models.CharField(max_length=200, null=True, blank=True)
    population = models.IntegerField(null=True, blank=True, default=0)
    elevation = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return u"{}: {}".format(self.id, self.name)


@python_2_unicode_compatible
class CountryInfo(models.Model):
    """ Country info from geonames. """
    iso_alpha2 = models.CharField(max_length=2)
    iso_alpha3 = models.CharField(max_length=3)
    iso_numeric = models.IntegerField()
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=200)
    capital = models.CharField(max_length=200)
    area = models.IntegerField(blank=True, null=True, default=0)
    population = models.IntegerField(blank=True, null=True, default=0)
    continent = models.CharField(max_length=2)
    languages = models.CharField(max_length=200)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AdminCode(models.Model):
    """ 1st level admin code areas. """
    name = models.CharField(max_length=200)
    name_std = models.CharField(max_length=200)
    country = models.CharField(max_length=3)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AltName(models.Model):
    """ Alternative names for objects. This will be used 'as is'. """
    geonameid = models.IntegerField()
    iso_code = models.CharField(max_length=7)
    altername = models.CharField(max_length=2000)
    language = models.CharField(max_length=10)
    is_preferred = models.BooleanField(default=False)
    is_short = models.BooleanField(default=False)
    is_colloquial = models.BooleanField(default=False)
    is_historic = models.BooleanField(default=False)

    def __str__(self):
        return self.altername
