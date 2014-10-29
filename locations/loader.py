import os, logging
from django.conf import settings
from django.contrib.auth.models import User
from geonames.models import *
from .models import *

# Let's work as superuser :)
admin = User.objects.get(pk=1)

# set custom log because of problems with django-one:
import logging
logging.basicConfig(filename=os.path.join(settings.BASE_DIR, 'logs', 'django.log'),
                   level=logging.INFO)


def get_translation(geonameid, country_code):
    """ Get native translations for geo name objects. """
    translation = None
    try:
        c = CountryInfo.objects.get(code=country_code)
        lang = c.languages.split(',')[0].split('-')[0]
    except CountryInfo.DoesNotExist:
        lang = None
    if lang is not None:
        try:
            translation = AltName.objects.filter(geonameid=geonameid, language=lang)
            translation = translation[0].altername
        except IndexError:
            translation = None
    return translation


def load_region_data(region, r_location):
    """
    This function takes AdminCode model instance as argument and creates city
    objects for entire region, excluding city districts. Additionally function
    takes location made based on region as argument to pass as parent for
    created cities.
    """
    city = GeoName.objects.filter(admin1=region.code, country=region.country)
    # Country capital region
    main = city.filter(feature_code='PPLC')
    # Regular admin region (e.g. state or voivodeship)
    if not main.count(): main = city.filter(feature_code='PPLA')
    forbidden = [x.admin2 for x in main]
    bad_codes = ['PPLX','PPLC','PPLA']
    city = city.exclude(admin2__in=forbidden).exclude(feature_code__in=bad_codes)
    # Get back main city removed by former query
    city = city | main
    for c in city:
        try:
            chk = Location.objects.get(pk=c.pk)
            logging.info("Location already exists: %s. Skipping", chk.name)
            continue
        except Location.DoesNotExist:
            pass

        try:
            trans = get_translation(c.pk, region.country)
            if trans is None: trans = c.name
            nl = Location.objects.create(
                id = c.pk,
                name      = trans,
                creator   = admin,
                kind      = c.feature_code,
                parent    = r_location,
                latitude  = c.latitude,
                longitude = c.longitude,
                country_code = c.country,
                population   = c.population
            )
            nl.save()
            logging.info("Created location: %s", nl.name)
        except Exception as ex:
            logging.error("Error creating location: %s - %s", c.name, repr(ex))


def load_country_data(code):
    """ 
    This function takes existing country code as argument and creates
    hierarchy - country/district/cities.
    """
    code = code.upper()
    country_info = CountryInfo.objects.get(code=code)
    regions_info = AdminCode.objects.filter(country=code)
    # Create location for country
    try:
        l = Location.objects.get(pk=country_info.pk)
        logging.info("Location already exists: %s. Skipping", l.name)
    except Location.DoesNotExist:
        trans = get_translation(country_info.pk, code)
        if trans is None: trans = country_info.name
        l = Location.objects.create(
            id = country_info.pk,
            name = trans,
            kind = 'country',
            country_code = country_info.code,
            creator = admin,
            population = country_info.population
        )
        l.save()
        logging.info("Created country location: %s", l.name)
    # Create related country instance
    try:
        l_country = Country.objects.get(location=l)
        logging.info("Related country already exists: %s. Skipping", l.name)
    except Country.DoesNotExist:
        l_country = Country.objects.create(code=code, location=l)
        l_country.save()
        logging.info("Created related country: %s", l.name)
    # Create location for every admin area and load cities
    for region in regions_info:
        try:
            nl = Location.objects.get(pk=region.pk)
            logging.info("Region already exists: %s. Skipping.", nl.name)
        except Location.DoesNotExist:
            trans = get_translation(region.pk, region.country)
            if trans is None: trans = region.name
            nl = Location.objects.create(
                id = region.pk,
                name = trans,
                kind = 'region',
                country_code = country_info.code,
                parent = l,
                creator = admin
            )
            nl.save()
            logging.info("Created region location: %s", nl.name)
        load_region_data(region, nl)


def load_translation_data(location_pk=None):
    """ This function updates location translations for registered languages. """
    langs = [x[0] for x in settings.LANGUAGES]
    if location_pk is not None:
        queryset = Location.objects.filter(pk=location_pk)
    else:
        queryset = Location.objects.all()
    for l in queryset:
        alt = AltName.objects.filter(geonameid=l.pk,
                                      language__in=langs)
        for a in alt:
            try:
                chk = l.names.get(pk=a.pk)
                logging.info("Translation %s exists. Skipping", a.pk)
            except AlterLocationName.DoesNotExist:
                alt_name = AlterLocationName.objects.create(
                    altername = a.altername,
                    language = a.language,
                )
                alt_name.save()
                l.names.add(alt_name)
                l.save()
                logging.info("Created translation %s for %s",
                             alt_name.language, l.pk)


def load():
    """ Loads entire data set for places above 1000 population. """
    for country in CountryInfo.objects.all():
        load_country_data(country.code)
