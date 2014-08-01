# -*- coding: utf-8 -*-
from django.db import models
from locations.models import Location


class Country(models.Model):
    """
    Podstawowy model na potrzeby geolokacji - przechowuje informacje wiążące
    kod języka przeglądarki z konkretnym krajem i parametrami wykorzystywanymi
    później przez mapę (w celu wycentrowania mapy pod konkretnego użytkownika
    i wyświetlenia miejsc, które szczególnie mogą go zainteresować).
    
    Model ten można (a nawet należy) połączyć z odpowiednią lokacją z bazy
    aplikacji 'locations'.
    """
    name = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    location = models.OneToOneField(Location, blank=True, null=True)

    def __unicode__(self):
        return self.name


class LanguageCode(models.Model):
    """
    Prosty model przechowujący kod języka i jego przynależność do kraju. W ten
    sposób będziemy mogli odwoływać się do kodów/krajów dzięki relacji.
    """
    code = models.CharField(max_length=10)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.code