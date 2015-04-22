# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context, Library, Node
from django.utils.translation import ugettext as _

from actstream.models import following

register = Library()


@register.simple_tag
def actstream(obj, stream_type='user'):
    """
	Creates activity stream placeholder with DOM attributes allowing scripts
    to fetch proper content.
	"""
    ct = ContentType.objects.get_for_model(obj).pk
    template = loader.get_template('activities/actstream.html')
    context = Context({'ct': ct, 'pk': obj.pk, 'type': stream_type, })
    return template.render(context)


@register.simple_tag(takes_context=True)
def follow_button(context, obj):
    user = context['user']
    if user.is_anonymous():
        return ''
    if obj in following(user):
        txt = _(u"Stop following")
    else:
        txt = _(u"Follow")
    return '<a class="civ-follow-btn" href="#" data-ct="{}" data-pk="{}">{}</a>'.format(
        ContentType.objects.get_for_model(obj).pk, obj.pk, txt)
