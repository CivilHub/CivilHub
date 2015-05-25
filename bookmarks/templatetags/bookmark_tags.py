# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Library
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from ..models import Bookmark

register = Library()

@register.simple_tag
def bookmark_form(instance=None, user=None):

    if not instance or not user: return ''

    if user.is_anonymous(): return ''

    ct = ContentType.objects.get_for_model(instance).pk
    pk = instance.pk

    try:
        bookmark = Bookmark.objects.filter(content_type=ct, object_id=pk, user=user)[0]
        cls = 'btn-bookmark btn-active-bookmark'
        title = _(u"Remove bookmark")
        bookmark_pk = bookmark.pk
    except IndexError:
        bookmark = None
        cls = 'btn-bookmark btn-add-bookmark'
        title = _(u"Add bookmark")
        bookmark_pk = ""

    return """<a href="#" class="{}" data-ct="{}" data-id="{}" data-pk="{}"
            data-toggle="tooltip" data-placement="bottom" title="{}">{}</a>
            """.format(cls, ct, pk, bookmark_pk, title, title)
