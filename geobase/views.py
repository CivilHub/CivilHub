# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import get_language


class IndexView(View):
    """
    Prosty widok wyświetlający statyczną stronę. Tymczasowo umieszczam tutaj
    informację o języku i lokalizacji użytkownika przechowywane w sesji w celu
    łatwiejszego podglądu.
    """
    def get(self, request):
        context = {'language': get_language()}
        return render(request, 'geobase/index.html', context)