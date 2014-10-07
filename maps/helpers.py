# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from locations.models import Location
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