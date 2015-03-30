# -*- coding: utf-8 -*-
from .models import Location

def get_most_followed(country_code=None, limit=20):
    """
    We download a list of the most often followed location. We can narrow
    the list to a certain country, to do so, we first type in the country
    and its capital city. it returns a LIST, not a QuerySet!
    """
    qs = Location.objects
    kinds = ['PPLC', 'country',]
    if country_code is None:
        return list(qs.all().order_by('-users')[:limit])
    main = list(qs.filter(country_code=country_code,
                  kind__in=kinds).order_by('kind'))
    full = list(qs.filter(country_code=country_code)\
                  .exclude(kind__in=kinds)\
                  .order_by('-users')[:limit-len(main)])
    return main + full
