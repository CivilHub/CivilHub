# -*- coding: utf-8 -*-
from django.template import Library
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.contenttypes.models import ContentType
from social.apps.django_app.default.models import UserSocialAuth

register = Library()

ALLOWABLE_VALUES = ("DEBUG", "COMMENT_PAGINATOR_LIMIT",)


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
def google_data(user=None):
    """ Prosty tag przechowujący dane uwierzytelniające dla Google. """
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
    """ Prosty tag do przekazania limitu paginacji dla skryptów. """
    if pg_type and pg_type == 'list':
        return settings.LIST_PAGINATION_LIMIT
    elif pg_type == 'stream':
        return settings.STREAM_PAGINATOR_LIMIT
    return settings.PAGE_PAGINATION_LIMIT


@register.simple_tag
def hreflang(request):
    """
    Prosty tag wyświetląjący tagi 'hreflang' dla każdej podstrony i każdego
    zarejestrowanego w systemie tłumaczenia. Jako parametr należy przekazać
    aktualny url, który znajdzie się w znaczniku.
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
    Tag, który automatycznie wypełnia menu z wyborem języków odnośnikami do
    wszystkich zarejestrowanych języków.
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
    return tags


@register.filter
def content_type(obj):
    """
    Get object's content type inside template. See:
    https://djangosnippets.org/snippets/3015/
    """
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)
