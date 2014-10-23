# -*- coding: utf-8 -*-
from django.db import models
from locations.models import Location


class Country(models.Model):
    """
    Podstawowy model na potrzeby geolokacji i dumpowania danych dla mapy
    do plików. Zasada działania jest prosta - dane dla mapy zostaną podzielone
    na kraje, a pliki odpowiadające odpowiednim typom zawartości z zapisanymi
    danymi o położeniu znajdą się w katalogu `data` aplikacji.
    
    Model przechowuje kod kraju, który powinien odpowiadać kodom zwracanym
    przez GeoIP. Na tej podstawie możemy połączyć fizyczną lokalizację
    użytkownika z miejscami, które mogłyby być dla niego interesujące.
    """
    code = models.CharField(max_length=2)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    location = models.OneToOneField(Location)

    def __unicode__(self):
        return self.code


class LanguageCode(models.Model):
    """
    Kody językowe ISO pobrane z bazy geonames. Umożliwią nam identyfikowanie
    języków i kojarzenie ich z językami zarejestrowanymi w Django w trakcie
    importu. Model przechowuje tylko języki z grupy podstawowej, tzn. posiadające
    dwuliterowe kody ISO-639-1, z innych nie korzystamy.
    """
    iso_code = models.CharField(max_length=2)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name
