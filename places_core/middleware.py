# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.utils import translation
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
    Middleware, który ustawia język sesji w zależności od wybranej subdomeny.
    """
    def process_request(self, request):
        code = request.META.get('HTTP_HOST', '').split('.')[0]
        if code in [x[0] for x in settings.LANGUAGES]:
            translation.activate(code)
