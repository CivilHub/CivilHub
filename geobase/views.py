# -*- coding: utf-8 -*-
import os, json
from django.shortcuts import render
from django.conf import settings
from django.views.generic import View
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.contrib.gis.geoip import GeoIP
from ipware.ip import get_ip
from rest_framework import serializers, permissions, viewsets
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer


class IndexView(View):
    """
    Prosty widok wyświetlający statyczną stronę. Tymczasowo umieszczam tutaj
    informację o języku i lokalizacji użytkownika przechowywane w sesji w celu
    łatwiejszego podglądu.
    """
    def find_user_country(self):
        """ Find Country object matching user's geolocation country code. """
        code = GeoIP().country_code(get_id(self.request))
        if code:
            try:
                country = Country.objects.get(code=code)
            except Country.DoesNotExist:
                country = None

    def get(self, request):
        g = GeoIP()
        ip = get_ip(request)
        context = {
            'ip': ip,
            'country': g.country(ip),
        }
        return render(request, 'geobase/index.html', context)


class CountryAPIViewSet(viewsets.ModelViewSet):
    """
    Tutaj kojarzymy kod państwa z GeoIP z naszym modelem lokalizacji. Model
    przechowuje informacje o startowej lokalizacji i powiększeniu mapy etc.
    Domyślnie prezentowana jest lista wszystkich państw w bazie. Umożliwia
    wyszukiwanie na podstawie country code (np. ?code=pl).
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        code = self.request.QUERY_PARAMS.get('code') or None
        if code:
            return Country.objects.filter(code=code.upper())
        return Country.objects.all()


class CountryCodeAPIViewSet(viewsets.ViewSet):
    """
    Prosty widok umożliwiający pobranie listy wszystkich krajów (nazwy w języku
    angielskim) wraz z ich dwuliterowymi kodami ISO.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request):
        f = open(os.path.join(settings.BASE_DIR, 'geobase/data/codes.json'))
        codes = f.read()
        f.close()
        return Response(json.loads(codes))
