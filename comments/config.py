# -*- coding: utf-8 -*-
from django.conf import settings

conf = {
    'PAGINATE_BY': 5,
    'EMAIL_NOTIFY': True,
}

def get_config(key):
    try:
        return getattr(settings, "COMMENT_%s" % key)
    except AttributeError:
        return conf.get(key)
