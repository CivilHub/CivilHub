# -*- coding: utf-8 -*-
from django.template import Library
from django.conf import settings

register = Library()


@register.simple_tag
def page_size(type=None):
    """ Prosty tag do przekazania limitu paginacji dla skryptów. """
    if type and type == 'list':
        return settings.LIST_PAGINATION_LIMIT
    return settings.PAGE_PAGINATION_LIMIT
