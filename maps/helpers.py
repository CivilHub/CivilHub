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


def make_region_cluster(city):
    """ This function takes region main location as argument and creates cache. """
    count = MapPointer.objects.filter(
        location__in=city.parent.get_children_id_list()).count()
    cache.set(str(city.pk) + '_childlist', count, timeout=None)
    return count


def create_region_clusters(lat, lng, zoom):
    """
    Create clusters for regions - usable in medium zoom. Function takes latitude
    and longitude of current map center as strings or numbers.
    """
    clusters = []
    if int(zoom) == 6: factor = 40.0
    elif int(zoom) > 6 and int(zoom) < 9: factor = 20.0
    else: factor = 10.0
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
        count = cache.get(str(l.pk) + '_childlist')
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
        l = Location.objects.get(country_code=c.code, kind='PPLC')
        cluster = {
            'lat': l.latitude,
            'lng': l.longitude,
            'counter': MapPointer.objects.filter(
                location__in=c.location.get_children_id_list()).count(),
        }
        clusters.append(cluster)
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
        results = cache.get("allcountries")
        if not results:
            results = create_country_clusters()
            cache.set("allcountries", results, timeout=None)
        return results
