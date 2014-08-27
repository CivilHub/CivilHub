# -*- coding: utf-8 -*-
from django.template import Library
from django.conf import settings

register = Library()


@register.simple_tag
def page_size(pg_type=None):
    """ Prosty tag do przekazania limitu paginacji dla skryptów. """
    if pg_type and pg_type == 'list':
        return settings.LIST_PAGINATION_LIMIT
    elif pg_type == 'stream':
        return settings.STREAM_PAGINATOR_LIMIT
    return settings.PAGE_PAGINATION_LIMIT
