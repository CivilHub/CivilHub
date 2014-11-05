# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.utils import translation
from django.shortcuts import redirect
from django.core.cache import cache
from django.db import connections, transaction
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions


def flush_cache():
    """
    Helper function to flush django default cache. WARNING: we suppose that
    you use default database connection for caching static content.
    """
    cache.clear()
    cursor = connections['default'].cursor()
    cursor.execute("TRUNCATE TABLE {};".format(
                    settings.CACHES['default']['LOCATION']})
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
        code = request.META.get('HTTP_HOST', '').split('.')[0]
        if code in [x[0] for x in settings.LANGUAGES]:
            url = request.META.get('HTTP_HOST', '').replace(code + '.', '')
            url += request.get_full_path()
            flush_cache()
            translation.activate(code)
            request.session['django_language'] = code
            if request.is_secure():
                return redirect('https://' + url)
            else:
                return redirect('http://' + url)
