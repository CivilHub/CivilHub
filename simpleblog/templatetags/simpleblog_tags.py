# -*- coding: utf-8 -*-
from ..models import BlogEntry
from django.template import Library
register = Library()

@register.simple_tag
def newscounter(obj):
    """ Count simpleblog entries published for selected content object.
	"""
    return BlogEntry.objects.get_published_in(obj).count()
