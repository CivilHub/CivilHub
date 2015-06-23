# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template import loader, Context, Library, Node
from django.utils.translation import ugettext as _

from actstream.models import following
from rest_framework.renderers import JSONRenderer

from ..helpers import get_first_page

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
    context['first_page'] = JSONRenderer().render(get_first_page(obj, stream_type))
    return template.render(context)


@register.simple_tag(takes_context=True)
def follow_button(context, obj):
    """
    Displays follow button for any target object. It is supposed
    to work with some kind of front-end scripts.
    """
    user = context['user']

    class_name = 'btn-follow'
    label_text = _(u"Follow")

    if user.is_anonymous():
        href = '/user/login/?next=' + context['request'].path
        return '<a class="{}" href="{}">{}</a>'.format(
            class_name, href, label_text)
    elif user == obj:
        return ''

    if obj in following(user):
        class_name = 'btn-unfollow'
        label_text = _(u"Stop following")

    content_type = ContentType.objects.get_for_model(obj).pk
    template = """<a class="civ-follow-btn {}"
         href="#"
         data-ct="{}"
         data-pk="{}">{}</a>"""

    return template.format(class_name, content_type, obj.pk, label_text)
