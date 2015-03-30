# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from ..models import CustomComment

from django.template import Library
register = Library()

@register.simple_tag
def get_comment_count(obj):
    """
    Returns the number of comments for a given object. The process is simplified
     - Choose only comments "first-level", without counting the answers.
    """
    ct = ContentType.objects.get_for_model(obj).pk
    return CustomComment.objects.filter(content_type_id=ct,
                                    object_pk=obj.pk).count()
