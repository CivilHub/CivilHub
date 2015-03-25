# -*- coding: utf-8 -*-
from django.shortcuts import render

from social import exceptions as social_exceptions
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware


class CivilAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            #return HttpResponse("catched: %s" % exception)
            ctx = {'exception': unicode(exception),}
            return render(request, 'userspace/social_exception.html', ctx)
        else:
            raise exception
