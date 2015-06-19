# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context
from django.utils.translation import ugettext as _

from rest_framework.renderers import JSONRenderer

from ..config import get_config
from ..models import CustomComment
from ..serializers import CommentDetailSerializer

from django.template import Library
register = Library()


@register.simple_tag
def get_comment_count(obj):
    """ Returns the number of comments for a given object.
    """
    ct = ContentType.objects.get_for_model(obj).pk
    return len(CustomComment.objects.filter(content_type_id=ct,
                                            object_pk=obj.pk))


@register.simple_tag(takes_context=True)
def commentarea(context, obj):
    """ Creates comment area for given object to be used later by scripts.
	"""
    ct = ContentType.objects.get_for_model(obj).pk
    template = loader.get_template('comments/commentarea.html')
    qs = CustomComment.objects.filter(content_type_id=ct,
                    object_pk=obj.pk).order_by('-submit_date')
    comments = qs.filter(parent__isnull=True)[:get_config('PAGINATE_BY')]
    data = {
        'has_next': len(qs) > get_config('PAGINATE_BY'),
        'results': CommentDetailSerializer(comments, many=True,
                                                     context=context).data, }
    ctx = Context({
        'user': context['user'],
        'ct': ct,
        'pk': obj.pk,
        'ab': ContentType.objects.get_for_model(CustomComment).pk,
        'count': len(qs),
        'comments': qs,
        'first_page': JSONRenderer().render(data),
    })
    return template.render(ctx)
