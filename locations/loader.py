from django.contrib.auth.models import User
from geonames.models import *
from .models import Location

# Let's work as superuser :)
admin = User.objects.get(pk=1)


def load_region_data(region, r_location):
    """
    This function takes AdminCode model instance as argument and creates city
    objects for entire region, excluding city districts. Additianally function
    takes location made based on region as argument to pass as parent for
    created cities.
    """
    city = GeoName.objects.filter(admin1=region.code)
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
        nl = Location.objects.create(
            id = c.pk,
            name      = c.name,
            creator   = admin,
            parent    = r_location,
            latitude  = c.latitude,
            longitude = c.longitude,
            country_code = c.country,
            population   = c.population
        )
        nl.save()


def load_country_data(code):
    """ 
    This function takes existing country code as argument and creates
    hierarchy - country/district/cities.
    """
    code = code.upper()
    country_info = CountryInfo.objects.get(code=code)
    regions_info = AdminCode.objects.filter(country=code)
    # Create location for country
    l = Location.objects.create(
        id = country_info.pk,
        name = country_info.name,
        country_code = country_info.code,
        creator = admin,
        population = country_info.population
    )
    l.save()
    # Create location for every admin area and load cities
    for region in regions_info:
        nl = Location.objects.create(
            id = region.pk,
            name = region.name,
            country_code = country_info.code,
            parent = l,
            creator = admin
        )
        nl.save()
        load_region_data(region, nl)


def load():
    """ Loads entire data set for places above 1000 population. """
    for country in CountryInfo.objects.all():
        load_country_data(country.code)
