# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from ..models import MapPointer

from django.template import Library
register = Library()

@register.assignment_tag
def get_map_pointers(obj):
    """ Returns a list of map points connected with the object. """
    return MapPointer.objects.for_model(obj)
