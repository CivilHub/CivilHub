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
from rest_framework import views as rest_views
from rest_framework.response import Response
from .models import Country
from .serializers import CountrySerializer, CountryCodeSerializer


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
    paginate_by = None
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)

    def get_queryset(self):
        code = self.request.QUERY_PARAMS.get('code') or None
        if code:
            return Country.objects.filter(code=code.upper())
        return Country.objects.all()


class CountryCodeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Prosty widok umożliwiający pobranie listy wszystkich krajów wraz 
    z ich dwuliterowymi kodami ISO.
    """
    queryset = Country.objects.all()
    serializer_class = CountryCodeSerializer
    paginate_by = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GeolocationAPIView(rest_views.APIView):
    """
    API Pozwalające sprawdzić lokalizację, w jakiej znajduje się użytkownik, na
    podstawie jego adresu IP. Adres należy przesłać w parametrach zapytania
    GET, np.:
    
    /api-geo/geoip/?ip=84.10.12.178
    
    W odpowiedzi otrzymamy obiekt z tzw. country code pobranym z bazy GEO IP oraz
    ID odpowiadającego mu kraju lub `null` jeżeli takiego kraju nie ma w bazie.
    Tylko zapytania GET/LIST! Widok bez paginacji.
    """
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request):
        ip = request.QUERY_PARAMS.get('ip')
        if ip:
            code = GeoIP().country(ip)['country_code']
            try:
                country = Country.objects.get(code=code).pk
            except Country.DoesNotExist:
                country = None
            return Response({'code':code,'country':country})
        return Response(_("Please provide an IP address"))
