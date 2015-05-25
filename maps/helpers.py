# -*- coding: utf-8 -*-
from django.core import cache
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from locations.models import Country, Location

from .models import MapPointer

import logging
logger = logging.getLogger('maps')

redis_cache = cache.get_cache('default')


def filter_markers(lat, lng, factor=1.0, filters=None, location_pk=None):
    """ 
    Simple marker list filter. It takes latitude and longitude as arguments and
    fetch pointers in distance of `factor` degrees from this point.
    
    Filters is array of content type id's to fetch. If None is set, nothing will be returned.
    
    If you pass location pk only markers related to this location will be fetched.
    """
    if filters is None:
        return []

    # if location_pk is not None:
    #     qs = MapPointer.objects.for_location(
    #         get_object_or_404(Location, pk=location_pk))
    # else:
    #     qs = MapPointer.objects.all()
    qs = MapPointer.objects.all()

    return qs.filter(
        latitude__gt=float(lat) - float(factor),
        latitude__lt=float(lat) + float(factor),
        longitude__gt=float(lng) - float(factor),
        longitude__lt=float(lng) + float(factor),
        content_type__in=[int(x) for x in filters.split(',') if x]
    )


def make_region_cluster(city):
    """ This function takes region main location as argument and creates cache. """
    count = MapPointer.objects.filter(
        location__in=city.parent.get_children_id_list()).count()
    redis_cache.set(str(city.pk) + '_childlist', count, timeout=None)
    logger.info("Created cluster for region {} with {} items".format(city.pk, count))
    return count


def create_region_clusters(lat, lng, zoom):
    """
    Create clusters for regions - usable in medium zoom. Function takes latitude
    and longitude of current map center as strings or numbers.
    """
    clusters = []

    if int(zoom) == 6:
        factor = 40.0
    elif int(zoom) > 6 and int(zoom) < 9:
        factor = 20.0
    else:
        factor = 10.0

    max_lat = float(lat) + factor
    max_lng = float(lng) + factor
    min_lat = float(lat) - factor
    min_lng = float(lng) - factor

    main_locations = Location.objects.filter(
        kind__in=['PPLA','PPLC'],
        latitude__gt=min_lat,
        latitude__lt=max_lat,
        longitude__gt=min_lng,
        longitude__lt=max_lng)

    for l in main_locations:
        # we can use this value directly - update signal takes care of cache.
        count = redis_cache.get(str(l.pk) + '_childlist')
        if count is None:
            count = make_region_cluster(l)
        cluster = {
            'lat': l.latitude,
            'lng': l.longitude,
            'counter': count,
        }
        clusters.append(cluster)
    return clusters


def create_country_clusters():
    """ Create clusters for all countries - for very low zoom level. """
    clusters = []
    main_locations = Country.objects.all()
    for c in main_locations:
        try:
            l = Location.objects.get(country_code=c.code, kind='PPLC')
            cluster = {
                'lat': l.latitude,
                'lng': l.longitude,
                'counter': MapPointer.objects.filter(
                    location__in=c.location.get_children_id_list()).count(),
            }
            clusters.append(cluster)
        except Location.DoesNotExist:
            logger.info(u"Cannot find capital location for %s" % c.code)
    redis_cache.set('allcountries', clusters, timeout=None)
    return clusters


def create_clusters(lat, lng, zoom):
    """
    Crate clusters for map when zoom is less then 10. As above, this function
    takes latitude, longitude and map zoom level as argments and returns array
    of marker positions along with number of items in requested region.
    """
    zoom = int(zoom)
    if zoom >= 6:
        return create_region_clusters(lat, lng, zoom)
    else:
        results = redis_cache.get("allcountries")
        if not results:
            results = create_country_clusters()
            redis_cache.set("allcountries", results, timeout=None)
        return results
