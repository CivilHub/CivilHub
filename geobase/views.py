# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.contrib.gis.geoip import GeoIP
from ipware.ip import get_ip
from rest_framework import serializers, permissions, viewsets
from .models import LanguageCode, Country
from .serializers import CountrySerializer


class IndexView(View):
    """
    Prosty widok wyświetlający statyczną stronę. Tymczasowo umieszczam tutaj
    informację o języku i lokalizacji użytkownika przechowywane w sesji w celu
    łatwiejszego podglądu.
    """
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
    Ten widok odpowiada za przekazywanie informacji o lokalizacji użytkownika
    na podstawie kodu języka (language code) przechowywanego w sesji. Wykorzys-
    tanie tego typu geolokacji nie wydaje się dobrym pomysłem dla apki mobilnej,
    OS-y mają swoje własne systemy namierzania i lepiej z nich skorzystać.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)