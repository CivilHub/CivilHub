# -*- coding: utf-8 -*-
from django.shortcuts import render

from social import exceptions as social_exceptions
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware


class CivilAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    """ Catch social auth exceptions instead of showing 500 page. """
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            ctx = {'exception': unicode(exception),}
            return render(request, 'userspace/social_exception.html', ctx)
        else:
            raise exception
