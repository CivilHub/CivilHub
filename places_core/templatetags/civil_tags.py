# -*- coding: utf-8 -*-
import json
import os

from django.template import Library
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from rest_framework.renderers import JSONRenderer
from social.apps.django_app.default.models import UserSocialAuth

from maps.models import MapPointer
from userspace.serializers import UserDetailSerializer


register = Library()
ALLOWABLE_VALUES = (
    "DEBUG",
    "COMMENT_PAGINATOR_LIMIT",
    "SOCIAL_AUTH_FACEBOOK_KEY",
)


@register.filter
def object_markers(obj):
    """ Fetches map points for objects for the usage of scripts. """
    if not obj or obj is None:
        return ""
    return mark_safe(json.dumps([{'lat': x.latitude, 'lng': x.longitude}\
        for x in MapPointer.objects.for_model(obj)]))


@register.simple_tag
def settings_value(name):
    """ Get single settings valued that is allowed to access. """
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''


@register.simple_tag
def js_path():
    """ Simple tag to change js path depending on settings. """
    if settings.DEBUG:
        return 'src'
    return 'dist'


@register.simple_tag
def module_path(module='default'):
    """ Return path to given js module. Use for require.js
    """
    from django.templatetags.static import static
    url = 'dist'
    if settings.DEBUG:
        url = 'src'
    return static('places_core/js/%s/%s.js' %(url, module))



@register.simple_tag
def require_config():
    f = open(os.path.join(settings.BASE_DIR, 'places_core/static/places_core/js/config.json'))
    conf = f.read()
    f.close()
    return """<script>require.config({});</script>""".format(conf)


@register.simple_tag
def google_data(user=None):
    """ A simple tag that stores verification data for Google """
    if user is None or user.is_anonymous(): return ''
    template = """<script>
        window.GOOGLE_DATA = {
            access_token: "{% token %}",
            client_id: "{% key %}",
            plus_scope: "{% scope %}",
            plus_id: "{% key %}"
        };
    </script>"""
    try:
        us = UserSocialAuth.objects.get(user=user, provider='google-plus')
        data = (
            settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY,
            us.extra_data['access_token'],
            settings.SOCIAL_AUTH_GOOGLE_PLUS_SCOPE,
        )
    except UserSocialAuth.DoesNotExist:
        data = ('','','')
    return template.replace('{% key %}', data[0]) \
                    .replace('{% token %}', data[1]) \
                    .replace('{% scope %}', ' '.join(data[2]))


@register.simple_tag
def page_size(pg_type=None):
    """ A simple tag to to convey a limit of pagination for scripts. """
    if pg_type and pg_type == 'list':
        return settings.LIST_PAGINATION_LIMIT
    elif pg_type == 'stream':
        return settings.STREAM_PAGINATOR_LIMIT
    return settings.PAGE_PAGINATION_LIMIT


@register.simple_tag
def hreflang(request):
    """
    A simple tag that displays tags 'hrefland' for each subpage and for each
    registered in the system translation. As a parameter the current url,
    present in the marker should, be passed.
    """
    host = request.META.get('HTTP_HOST', '').split('.')
    protocol = 'https' if request.is_secure() else 'http'
    if len(host[0]) == 2: del(host[0])
    host = '.'.join(host) + request.path
    tags = ['<link rel="alternate" href="'+protocol+'://'+host+'" hreflang="x-default" />',]
    template = '<link rel="alternate" href="'+protocol+'://{% url %}" hreflang="{% lang %}" />'

    for l in settings.LANGUAGES:
        url = '.'.join([l[0], host])
        tags.append(template.replace('{% url %}', url).replace('{% lang %}', l[0]))

    return "".join(tags)


@register.simple_tag
def langlist(request):
    """
    A tag that automatically fills in the menu with links of language selection
    for each registered language.
    """
    tags = ''
    tpl = """<li data-code="{% code %}"{% active %}>
                <a href="{% url %}" onClick="ga('send', 'event', 'language-{% CODE %}', 'click', 'language-{% CODE %}');">
                    <img alt="{% name %}" src="{% src %}"><span>{% name %}</span>
                </a>
            </li>"""
    proto_src = settings.STATIC_URL + 'places_core/img/lang/{% code %}.png'
    host = request.META.get('HTTP_HOST', '').split('.')
    protocol = 'https' if request.is_secure() else 'http'
    if len(host[0]) == 2: del(host[0])

    for l in settings.LANGUAGES:
        addr = list(host)
        addr.insert(0, l[0])
        addr = protocol + '://' + ('.'.join(addr)) + str(request.get_full_path())
        active = ' class="selected"' if l[0] == get_language() else ''
        src = proto_src.replace('{% code %}', l[0])
        tags += tpl.replace('{% code %}', l[0]) \
                   .replace('{% name %}', l[1]) \
                   .replace('{% src %}', src) \
                   .replace('{% active %}', active) \
                   .replace('{% url %}', addr) \
                   .replace('{% CODE %}', l[0].upper())
    transifex_url = '//www.transifex.com/projects/p/civilhub/'
    transifex_label = _(u"Help in translate")
    tags += '<a href="{}" target="_blank" class="help_translate">{}</a>'\
            .format(transifex_url, transifex_label)
    return tags


@register.simple_tag
def obj_ct_id(model_name):

    from articles.models import Article
    from ideas.models import Idea
    from blog.models import News
    from polls.models import Poll
    from topics.models import Discussion

    if model_name == 'article':
        model = Article
    elif model_name == 'idea':
        model = Idea
    elif model_name == 'news':
        model = News
    elif model_name == 'poll':
        model = Poll
    elif model_name == 'discussion':
        model = Discussion
    else:
        model = None

    if model is not None:
        return ContentType.objects.get_for_model(model).pk
    else:
        return 0


@register.filter
def content_type(obj):
    """
    Get object's content type inside template. See:
    https://djangosnippets.org/snippets/3015/
    """
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)


@register.simple_tag
def report_link(obj):
    """
    Creates abuse report link for given object.
    """
    if not obj:
        return False
    ct = ContentType.objects.get_for_model(obj)
    return '<a href="#" class="abuse-link" data-ct="{}" data-pk="{}">{}</a>'\
        .format(ct.pk, obj.pk, _(u"Report abuse"))


@register.simple_tag
def get_verbose_name(object):
    return object._meta.verbose_name.title()


@register.simple_tag(takes_context=True)
def js_userdata(context):
    """
    This tag is very useful for passing data of logged-in user into javascript
    context. It presents vital user info in common JSON syntax.
    """
    user = context['user']

    if user.is_anonymous():
        return ""

    serializer = UserDetailSerializer(user)

    return JSONRenderer().render(serializer.data)
