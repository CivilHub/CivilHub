# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import Library

from ..models import Visit

register = Library()


def render_node(counter, instance):
    """
    Helper function - adds data-ct and data-pk to HTML attributes.
    """
    ct = ContentType.objects.get_for_model(instance).pk
    return '<span class="visit-counter" data-ct="{}" data-pk="{}">{}</span>'\
        .format(ct, instance.pk, counter)


@register.simple_tag
def visit_counter(obj):
    """
    Returns total visit count for specified object.
    """
    return render_node(Visit.objects.count_for_object(obj), obj)


@register.simple_tag
def unique_counter(obj):
    """
    Returns visit count unique for ip addresses.
    """
    return render_node(Visit.objects.count_unique_for_object(obj), obj)
