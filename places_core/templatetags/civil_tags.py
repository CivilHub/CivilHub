# -*- coding: utf-8 -*-
from django.template import Library
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib.contenttypes.models import ContentType
from userspace.models import Bookmark

register = Library()


@register.simple_tag
def page_size(pg_type=None):
    """ Prosty tag do przekazania limitu paginacji dla skryptów. """
    if pg_type and pg_type == 'list':
        return settings.LIST_PAGINATION_LIMIT
    elif pg_type == 'stream':
        return settings.STREAM_PAGINATOR_LIMIT
    return settings.PAGE_PAGINATION_LIMIT


@register.simple_tag
def bookmark_form(instance=None, user=None):
    
    if not instance or not user: return ''

    if user.is_anonymous(): return ''
    
    ct = ContentType.objects.get_for_model(instance).pk
    pk = instance.pk
    
    if len(Bookmark.objects.filter(content_type=ct, object_id=pk, user=user)):
        cls = 'btn-remove-bookmark'
        text = _("Remove bookmark")
    else:
        cls = 'btn-add-bookmark'
        text = _("Bookmark")
        
    return '<a href="#" class="' + cls + '" data-ct="' + str(ct) + \
            '" data-id="' + str(pk) + '">' + text + '</a>'


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
    tpl = '<li data-code="{% code %}"{% active %}><a href="{% url %}"><img alt="{% name %}" src="{% src %}"><span>{% name %}</span></a></li>'
    proto_src = settings.STATIC_URL + 'places_core/img/lang/{% code %}.png'
    host = request.META.get('HTTP_HOST', '').split('.')
    protocol = 'https' if request.is_secure() else 'http'
    if len(host[0]) == 2: del(host[0])
    
    for l in settings.LANGUAGES:
        addr = list(host)
        addr.insert(0, l[0])
        addr = '.'.join(addr)
        addr = protocol + '://' + addr
        active = ' class="selected"' if l[0] == get_language() else ''
        src = proto_src.replace('{% code %}', l[0])
        tags += tpl.replace('{% code %}', l[0]) \
                   .replace('{% name %}', l[1]) \
                   .replace('{% src %}', src) \
                   .replace('{% active %}', active) \
                   .replace('{% url %}', addr)
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
