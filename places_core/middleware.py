# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils import translation
from django.shortcuts import redirect
from django.core.cache import cache
from django.db import connections, transaction
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions

from .views import redirect_404


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
    Middleware that sets the session language depending on the subdomain.
    """
    def process_request(self, request):
        host = request.META.get('HTTP_HOST', '')
        code = host.split('.')[0]
        if translation.check_for_language(code):
            translation.activate(code)
            t = re.compile('/(login|register)/')
            path_test = t.search(request.get_full_path())
            if path_test is not None or request.user.is_authenticated():
                host = host.replace(code + '.', '')
                if request.is_secure():
                    next = 'https://' + host + request.get_full_path()
                else:
                    next = 'http://' + host + request.get_full_path()
                return HttpResponseRedirect(next)


class Redirect404Middleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # No need to check for a flatpage for non-404 responses.
        try:
            return redirect_404(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
