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
    Main site view. Depending on whether the user is already a logged-in user
    or not, it presents a registration forum or a subpage of user activities.
    """
    template_name = 'staticpages/pages/home.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/activity/')
        return super(HomeView, self).get(request)


class PageView(View):
    """
    A basic view that loads a single page.
    """
    page = None

    def get_all_pages(self):
        """
        Searches through a folder in order to find static pages.
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
