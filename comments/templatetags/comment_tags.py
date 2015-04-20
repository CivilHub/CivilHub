# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context
from django.utils.translation import ugettext as _

from ..models import CustomComment

from django.template import Library
register = Library()


@register.simple_tag
def get_comment_count(obj):
    """
    Returns the number of comments for a given object.
    """
    ct = ContentType.objects.get_for_model(obj).pk
    return len(CustomComment.objects.filter(content_type_id=ct,
                                            object_pk=obj.pk))


@register.simple_tag
def commentarea(obj):
    """
	Creates comment area for given object to be used later by scripts.
	"""
    ct = ContentType.objects.get_for_model(obj).pk
    template = loader.get_template('comments/commentarea.html')
    context = Context({
        'ct': ct,
        'pk': obj.pk,
        'count': len(CustomComment.objects.filter(content_type_id=ct,
                                                  object_pk=obj.pk)),
    })
    return template.render(context)
