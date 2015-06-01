# -*- coding: utf-8 -*-
import math

from django.core.cache import get_cache

from locations.models import Location
from places_core.helpers import round_to_ten

from models import MapPointer

cache = get_cache('default')


def round_to(n, precision):
    """ Round floating point number to selected precision.
    """
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision


def round_to_05(n):
    """ Round float to nearest 0.5.
    """
    return round_to(n, 0.5)


def get_boundaries(ne, sw):
    """ A little helper to decipher GET params into tuples.
    """
    return {
        'ne': tuple(float(x) for x in ne.split('x')),
        'sw': tuple(float(x) for x in sw.split('x')), }


def filter_markers(south_west, north_east):
    """ Filter markers for selected viewport.
    """
    boundaries = get_boundaries(south_west, north_east)
    min_lat, min_lng = boundaries['ne']
    max_lat, max_lng = boundaries['sw']
    diff = max([max_lat - min_lat, max_lng - min_lng, ]) / 4
    qs = MapPointer.objects.filter(latitude__gte=min_lat - diff,
                                   latitude__lte=max_lat + diff,
                                   longitude__gte=min_lng - diff,
                                   longitude__lte=max_lng + diff)
    return qs


def find_region_cities(south_west, north_east):
    """ Find main region and country cities for given lat/lng boudaries.
    """
    kinds = ['PPLC', 'PPLA', ]
    boundaries = get_boundaries(south_west, north_east)
    min_lat, min_lng = boundaries['ne']
    max_lat, max_lng = boundaries['sw']
    diff = max([max_lat - min_lat, max_lng - min_lng, ]) / 4
    return Location.objects.filter(
        kind__in=kinds,
        latitude__gte=min_lat - diff,
        latitude__lte=max_lat + diff,
        longitude__gte=min_lng - diff,
        longitude__lte=max_lng + diff)


def create_cluster(main_city):
    """ Creates cluster for given main city (either capital or region capital).
    """
    id_list = main_city.parent.get_children_id_list()
    return {
        'id': main_city.pk,
        'lat': main_city.latitude,
        'lng': main_city.longitude,
        'count': len(MapPointer.objects.filter(location__pk__in=id_list)),
    }


def update_region_cluster(main_city):
    """ Updates or creates cache entry for selected city cluster.
    """
    cluster = create_cluster(main_city)
    cache.set("clusters_{}".format(main_city.pk), cluster, timeout=None)
    return cluster


def create_region_clusters():
    """ Creates entire set of clusters for all countries in database. Use this
        carefully as this may take A LONG time.
    """
    main_cities = Location.objects.filter(kind__in=['PPLA', 'PPLC', ])
    clusters = []
    for city in main_cities:
        clusters.append(update_region_cluster(city))
    return clusters


def get_clusters(south_west, north_east):
    """ Try to serve cached content first, and fallback to creating new clusters.
        This is not recommended - it is VERY heavy database operation.
    """
    main_cities = find_region_cities(south_west, north_east)
    clusters = []
    for city in main_cities:
        cluster = cache.get('clusters_{}'.format(city.pk))
        if cluster is None:
            cluster = update_region_cluster(city)
        clusters.append(cluster)
    return clusters
