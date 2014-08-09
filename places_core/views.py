# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.shortcuts import render
from .models import AbuseReport
from .forms import AbuseReportForm
# REST API
from rest_framework import viewsets
from rest_framework import permissions as rest_permissions
from .serializers import ContentTypeSerializer


class ContentTypeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Widok umożliwiający pobieranie ID typów zawartości na podstawie nazwy
    aplikacji lub modelu i vice-versa. Tylko zapytania GET! Domyślnie listowane
    są wszystkie typy zawartości.
    
    Wyszukiwać można na dwa sposoby, dodając parametry GET do zapytania:
        1. Podać ID konkretnego typu zawartości (np. ?id=8)
        2. Podać nazwę aplikacji i modelu (np. ?app_label=ideas&model=idea)
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


def report_sent(request):
    ctx = {'title': _('Report sent')}
    return render(request, 'places_core/report-sent.html', ctx)
