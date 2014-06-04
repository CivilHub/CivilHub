# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.generic import View

PAGE_DIR = os.path.join(settings.BASE_DIR, 'staticpages/templates/staticpages/pages/')

class PageView(View):
    """
    Podstawowy widok ładujący pojedynczą stronę.
    """
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
        if page == None:
            pages = self.get_all_pages()
            return render(request, 'staticpages/pages/home.html', {'pages':pages})
        else:
            try:
                template_name = 'staticpages/pages/' + page + '.html'
                return render(request, template_name)
            except Exception as ex:
                return HttpResponseNotFound()
