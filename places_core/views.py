# -*- coding: utf-8 -*-
import json

from django.core.cache import cache
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.utils.translation import check_for_language
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.shortcuts import render

from .models import AbuseReport
from .forms import AbuseReportForm


def flush_page_cache():
    """
    This function clears the cache saved in the template
    when we change the language of the site.
    """
    langs = [x[0] for x in settings.LANGUAGES]
    sections = ['home',]
    for l in langs:
        for s in sections:
            key = '_'.join([s, l])
            cache.delete(key)


@csrf_exempt
def set_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            flush_page_cache()
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                                lang_code, 365*24*60*60,
                                domain = settings.SESSION_COOKIE_DOMAIN)
    return response


class FileServeView(View):
    """ A view that serves static files. """
    http_method_names = [u'get', u'head', u'options', u'trace']
    filename = None

    def get(self, request, filename=None):
        if filename: self.filename = filename
        try:
            f = open(self.filename)
            content = f.read()
            f.close()
        except IOError:
            return HttpResponseNotFound()
        return HttpResponse(content, content_type="text/plain")


class CreateAbuseReport(CreateView):
    """
    Static form to create abuse reports for different ContentTypes.
    """
    model = AbuseReport
    form_class = AbuseReportForm
    template_name = 'places_core/abuse-report.html'
    success_url = '/report/sent/'

    def get(self, request, *args, **kwargs):
        app_label = kwargs['app_label']
        model_label = kwargs['model_label']
        content_type = ContentType.objects.get_by_natural_key(app_label,
                                                              model_label)
        ctx = {
                'title': _('Send abuse report'),
                'form': AbuseReportForm(initial={
                    'content_type': content_type,
                    'object_pk': kwargs['object_pk'],
                }),
            }
        return render(request, self.template_name, ctx)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sender = self.request.user
        obj.site = get_current_site(self.request)
        obj.save()
        return super(CreateAbuseReport, self).form_valid(form)

    def pre_save(self, obj):
        obj.sender = self.request.user
        obj.site = Site.objects.get_current().domain


class ReportView(CreateView):
    """
    Create abuse reports for different content types.
    """
    model = AbuseReport
    template_name = 'places_core/abuse-window-modal.html'
    form_class = AbuseReportForm

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_anonymous():
            raise Http404
        return super(ReportView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super(ReportView, self).get_initial()
        initial['content_type'] = self.kwargs.get('ct')
        initial['object_pk'] = self.kwargs.get('pk')
        return initial

    def form_invalid(self, form):
        if self.request.is_ajax():
            context = json.dumps({
                'success': False,
                'errors': form.errors,
            })
            return HttpResponse(context, content_type="application/json")
        return super(ReportView, self).form_invalid()

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.sender = self.request.user
        obj.site = Site.objects.get_current()
        obj.save()
        if self.request.is_ajax():
            context = json.dumps({
                'success': True,
                'message': _(u'Report sent'),
            })
            return HttpResponse(context, content_type="application/json")
        return super(ReportView, self).form_valid()
