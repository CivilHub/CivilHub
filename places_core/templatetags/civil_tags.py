# -*- coding: utf-8 -*-
import json
import os

from django.template import Library
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.renderers import JSONRenderer
from social.apps.django_app.default.models import UserSocialAuth

from maps.models import MapPointer
from userspace.serializers import UserDetailSerializer

from ..utils import get_current_version


register = Library()
ALLOWABLE_VALUES = (
    "DEBUG",
    "COMMENT_PAGINATOR_LIMIT",
    "SOCIAL_AUTH_FACEBOOK_KEY",
)


@register.simple_tag(takes_context=True)
def paginator_url(context, page=1):
    """ Creates proper url for pagination entries with GET params etc.
    """
    request = context.get('request')
    params = ["{}={}".format(k, v) for k, v in \
                request.GET.iteritems() if k != 'page']
    if not len(params):
        return '?page={}'.format(page)
    return "?{}&page={}".format("&".join(params), page)


@register.simple_tag(takes_context=True)
def form_from_params(context):
    """ This tag is similar to the above, but intended to use with forms.

    Form should use GET method. This tag creates additional hidden input fields
    for form body based on params found in current URL. Usually used in search
    filter forms as it ignores `q` parameter.
    """
    html = ""
    request = context.get('request')
    for k, v in request.GET.iteritems():
        if k != 'q':
            html += '<input type="hidden" name="{}" value="{}">'.format(k, v)
    return html


@register.simple_tag(takes_context=True)
def url_from_params(context, param=None, value=None):
    """ Another tag usefull for creating links with GET params.
    """
    request = context.get('request')
    params = ["{}={}".format(k, v) for k, v in \
                request.GET.iteritems() if k != param]
    if not len(params):
        return '?{}={}'.format(param, value)
    return "?{}&{}={}".format("&".join(params), param, value)


@register.filter
def as_fck_str(val):
    """ Yes, there is actually NO WAY to compare selected model in model choice
        field with option elements value attributes, because one is A NUMBER
        and the latter is STRING. This is SICK!
    """
    return str(val)


@register.simple_tag()
def version():
    return get_current_version()


@register.simple_tag(takes_context=True)
def embed_url(context, obj):
    ct = ContentType.objects.get_for_model(obj)
    site = get_current_site(context['request'])
    pref = 'https' if context['request'].is_secure() else 'http'
    return "{}://{}{}".format(pref, site.domain, reverse('locations:get-widget',
                            kwargs={'ct': ct.pk, 'pk': obj.pk, }))


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
    return static('places_core/js/%s/%s.js?V=%s' % (url, module, get_current_version()))


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
    help_translate_url = '//civilhub.org/for-translators/'
    help_translate_label = _(u"Help in translation")
    tags += '<a href="{}" target="_blank" class="help_translate">{}</a>'\
            .format(help_translate_url, help_translate_label)
    return tags


@register.simple_tag
def obj_ct_id(model_name):

    from articles.models import Article
    from ideas.models import Idea
    from blog.models import News
    from polls.models import Poll
    from topics.models import Discussion
    from locations.models import Location

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
    elif model_name == 'location':
        model = Location
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
    try:
        return object._meta.verbose_name.title()
    except AttributeError:
        return ""


@register.simple_tag(takes_context=True)
def js_userdata(context):
    """
    This tag is very useful for passing data of logged-in user into javascript
    context. It presents vital user info in common JSON syntax.
    """
    user = context['user']

    if user.is_anonymous():
        return "[]"

    serializer = UserDetailSerializer(user)

    return JSONRenderer().render(serializer.data)
