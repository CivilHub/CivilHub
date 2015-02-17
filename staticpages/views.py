# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView, View


PAGE_DIR = os.path.join(settings.BASE_DIR, 'staticpages/templates/staticpages/pages/')


class HomeView(TemplateView):
    """
    Widok głównej strony. W zależności od tego, czy użytkownik jest już zalogo-
    wanym użytkownikiem, czy nie, prezentuje formularz rejestracji lub stronę
    aktywności użytkownika.
    """
    template_name = 'staticpages/pages/home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('user:profile', request.user.username)
        return super(HomeView, self).get(request)


class PageView(View):
    """
    Podstawowy widok ładujący pojedynczą stronę.
    """
    page = None

    def get_all_pages(self):
        """
        Przeszukuje folder w poszukiwaniu stron statycznych.
        """
        pages = []
        for page in os.listdir(PAGE_DIR):
            pages.append({
                'url': str(reverse('pages:page', kwargs={'page': page[:4]})),
                'name': page[:4],
            })
        return pages

    def get(self, request, page=None):
        if self.page: page = self.page
        if page == None:
            return render(request, 'staticpages/pages/home.html')
        else:
            try:
                template_name = 'staticpages/pages/' + page + '.html'
                return render(request, template_name)
            except Exception as ex:
                return HttpResponseNotFound()
