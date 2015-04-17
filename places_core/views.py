# -*- coding: utf-8 -*-
import json
from urllib2 import unquote

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions as rest_permissions

from .models import AbuseReport
from .forms import AbuseReportForm
from .serializers import ContentTypeSerializer, PaginatedSearchSerializer


def flush_page_cache():
    """ This function clears the cache saved in the template when we change the language of the site. """
    langs = [x[0] for x in settings.LANGUAGES]
    sections = ['home',]
    for l in langs:
        for s in sections:
            key = '_'.join([s, l])
            cache.delete(key)


@csrf_exempt
def token_check(request):
    """
    We check and log authentication tokens from external servers.
    We need to rememebr to delete this later!!!
    """
    import json, logging
    from django.utils import timezone

    logger = logging.getLogger('tokens')

    if request.method == 'POST':
        token = request.POST.get('token')
        logger.info(u"[{}]: {}".format(timezone.now(), token))
        return HttpResponse(json.dumps({'token': token}),
                            content_type="application/json")
    return render(request, 'places_core/fbtest.html', {})


class SearchResultsAPIViewSet(viewsets.ViewSet):
    """
    A serch enginge for the mobile application. It allows to check search results
    by specifing the correct entry for the search (of course in a url-friendly manner).
    It returns a list of found objects that contain the fields 'name', 'content_type'
    and 'object_pk'. The system recognizes phrases passed through such functions as
    'encodeURI', 'encodeURIComponent' or 'urlencode'.
    #### Sample query:
    ```/api-core/search/?q=warszawa```
    """
    serializer_class = PaginatedSearchSerializer
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,)

    def _get_model_labels(self, ct_list):
        if not len(ct_list):
            return None
        return [ContentType.objects.get(pk=x).model_class() for x in ct_list]

    def get_queryset(self):
        from haystack.query import SearchQuerySet
        try:
            query_term = unquote(self.request.QUERY_PARAMS.get('q'))
            sqs = SearchQuerySet().filter(content=query_term)
            types = self.request.QUERY_PARAMS.get('ct', '').split(',')
            models = self._get_model_labels([int(x) for x in types if x])
            if models is not None:
                sqs = sqs.models(*models)
        except Exception:
            sqs = []
        return sqs

    def list(self, request):
        sqs = [x for x in self.get_queryset() if x.object is not None]
        paginator = Paginator(sqs, settings.LIST_PAGINATION_LIMIT)
        page = request.QUERY_PARAMS.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(results,
                                            context={'request': request})
        return Response(serializer.data)


class ContentTypeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A view that allows to download content ID types based on the application name
    or model and vice-versa. Only GET queries! By default all types are listed.

    It is possible to search in two ways, by adding GET parameters to the query:
        1. Pass an ID of a concrete content type (e.g. ?id=8)
        2. Pass the name of the application and model (e.g. ?app_label=ideas&model=idea)
    """
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    paginate_by = None

    def get_queryset(self):
        app_label = self.request.QUERY_PARAMS.get('app_label', None)
        model = self.request.QUERY_PARAMS.get('model', None)
        id = self.request.QUERY_PARAMS.get('id', None)
        if id:
            return ContentType.objects.filter(pk=id)
        elif app_label and model:
            return ContentType.objects.filter(app_label=app_label, model=model)
        else:
            return ContentType.objects.all()


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
            flush_page_cache();
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


class TestView(View):
    """ This is test. """
    template_name = 'staticpages/pages/testpage.html'
    def get(self, request):
        """ Convert Django messages into flash messages from our js framework. """
        from django.contrib import messages
        from django.shortcuts import render
        messages.add_message(request, messages.INFO, 'Message sent')
        messages.add_message(request, messages.WARNING, 'Message sent')
        messages.add_message(request, messages.ERROR, 'Message sent')
        messages.add_message(request, messages.SUCCESS, 'Message sent')
        return render(request, self.template_name, {})
