# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import translation
from django.shortcuts import redirect
from django.core.cache import cache
from django.db import connections, transaction
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions


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
