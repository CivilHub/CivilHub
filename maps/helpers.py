# -*- coding: utf-8 -*-
from .models import MapPointer

def filter_markers(lat, lng, factor=1.0, filters=None):
    """ 
    Simple marker list filter. It takes latitude and longitude of point as 
    arguments and fetching pointers in distance of `factor` degrees from this
    point.
    """
    f = float(factor)
    queryset = MapPointer.objects.filter(latitude__gt = float(lat) - f) \
                                .filter(latitude__lt  = float(lat) + f) \
                                .filter(longitude__gt = float(lng) - f) \
                                .filter(longitude__lt = float(lng) + f)

    if filters is not None:
        filters = [int(x) for x in filters.split(',') if x]
        queryset = queryset.filter(content_type__in=filters)
    
    return queryset