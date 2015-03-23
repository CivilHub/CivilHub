# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

from ..models import CustomComment

from django.template import Library
register = Library()

@register.simple_tag
def get_comment_count(obj):
    """
    Zwraca liczbę komentarzy dla podanego obiektu. Sposób jest uproszczony
    - wybieramy tylko komentarze "pierwszego poziomu", bez liczenia odpowiedzi.
    """
    ct = ContentType.objects.get_for_model(obj).pk
    return CustomComment.objects.filter(content_type_id=ct,
                                    object_pk=obj.pk).count()
