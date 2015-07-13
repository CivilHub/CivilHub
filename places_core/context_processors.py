# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site


def site_processor(request):
    """ Returns current site (protocol and domain name). Useful for loading
        external resources in email templates and REST API. See:
        http://stackoverflow.com/questions/7466684/is-the-current-site-accessible-from-a-template
    """
    prefix = 'https' if request.is_secure() else 'http'
    return {'site': "{}://{}".format(prefix, Site.objects.get_current()), }


def debug_processor(request):
    """ Return DEBUG value from settings file.
    """
    return {'DEBUG': settings.DEBUG, }
