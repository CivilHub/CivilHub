# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation
from django.shortcuts import redirect
from django.core.cache import cache
from django.db import connections, transaction
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions

import logging, os
LOG = os.path.join(settings.BASE_DIR, 'logs/django.log')
logging.basicConfig(filename = LOG, level = logging.INFO)


def flush_cache():
    """
    Helper function to flush django default cache. WARNING: we suppose that
    you use default database connection for caching static content.
    """
    cache.clear()
    cursor = connections['default'].cursor()
    cursor.execute("TRUNCATE TABLE {};".format(
                    settings.CACHES['default']['LOCATION']))
    transaction.commit_unless_managed(using='default') 


class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    """
    Custom exception to handle social auth logging and authorization errors.
    It is meant to be further extended by providing template/view to display
    errors.
    """
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, 'AuthException'):
            return HttpResponse("Social auth exception: %s" % exception)
        else:
            raise exception


class SubdomainMiddleware(object):
    """
    Middleware, który ustawia język sesji w zależności od wybranej subdomeny.
    """
    def process_request(self, request):
        code = request.GET.get('lang', None)
        if code is None:
            code = request.META.get('HTTP_HOST', '').split('.')[0]
        if translation.check_for_language(code):
            next = request.get_full_path() \
                    .replace('?lang={}'.format(code), '') \
                    .replace('&lang={}'.format(code), '')
            response = HttpResponseRedirect(next)
            flush_cache()
            translation.activate(code)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, code, 365*24*60*60)
            logging.info("Language set to {}".format(code))
            return response
