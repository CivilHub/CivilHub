# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from locations.models import Country, Location
from .models import MapPointer

def filter_markers(lat, lng, factor=1.0, filters=None, location=None):
    """ 
    Simple marker list filter. It takes latitude and longitude of point as 
    arguments and fetching pointers in distance of `factor` degrees from this
    point.
    
    Filters is array of content type id's to fetch.
    
    If you pass location pk only markers related to this location will be
    fetched.
    """
    f = float(factor)

    if location is not None:
        l = Location.objects.get(pk=location)
        queryset = MapPointer.objects.for_location(l)
    else:
        queryset = MapPointer.objects.all()

    queryset = queryset.filter(latitude__gt = float(lat) - f) \
                        .filter(latitude__lt  = float(lat) + f) \
                        .filter(longitude__gt = float(lng) - f) \
                        .filter(longitude__lt = float(lng) + f)

    if filters is not None:
        filters = [int(x) for x in filters.split(',') if x]
        queryset = queryset.filter(content_type__in=filters)

    return queryset


def create_region_clusters(lat, lng, filters=None):
    clusters = []
    max_lat = float(lat) + 10.0
    max_lng = float(lng) + 10.0
    min_lat = float(lat) - 10.0
    min_lng = float(lng) - 10.0

    main_locations = Location.objects.filter(
        kind__in=['PPLA','PPLC'],
        latitude__gt=min_lat,
        latitude__lt=max_lat,
        longitude__gt=min_lng,
        longitude__lt=max_lng)

    for l in main_locations:
        count = cache.get(str(l.pk) + '_childlist')
        if count is None:
            count = MapPointer.objects.filter(location__in=l.parent.get_children_id_list()).count()
            cache.set(str(l.pk) + '_childlist', count, timeout=None)
        cluster = {
            'lat': l.latitude,
            'lng': l.longitude,
            'counter': count,
        }
        clusters.append(cluster)
    return clusters


def create_country_clusters(filters=None):
    clusters = []
    main_locations = Country.objects.all()
    for c in main_locations:
        l = Location.objects.get(country_code=c.code, kind='PPLC')
        cluster = {
            'lat': l.latitude,
            'lng': l.longitude,
            'counter': MapPointer.objects.filter(location__in=c.location.get_children_id_list()).count(),
        }
        clusters.append(cluster)
    return clusters


def create_clusters(lat, lng, zoom, filters=None):
    """
    Crate clusters for map when zoom is less then 10. As above, this function
    takes latitude, longitude and map zoom level as argments and returns array
    of marker positions along with number of items in requested region.
    """
    zoom = int(zoom)
    if zoom >= 5:
        return create_region_clusters(lat, lng, filters)
    else:
        results = cache.get("allcountries")
        if not results:
            results = create_country_clusters(filters)
            cache.set("allcountries", results, timeout=None)
        return results
