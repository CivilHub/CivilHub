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
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    location = models.OneToOneField(Location)

    def __unicode__(self):
        return self.name