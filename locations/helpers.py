# -*- coding: utf-8 -*-
from .models import Location

def get_most_followed(country_code=None, limit=20):
    """
    Pobieramy listę najchętniej obserwowanych lokalizacji. Możemy zawęzić
    listę do konkretnego kraju, wówczas w pierwszej kolejności podajemy kraj
    oraz jego stolicę. Zwraca LISTĘ, nie QuerySet!
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
