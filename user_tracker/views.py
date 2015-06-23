# -*- coding: utf-8 -*-
import json

from django.core import serializers
from django.http import Http404, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.detail import SingleObjectMixin

from .models import Visitor


class VisitorsMainView(TemplateView):
    """ This view allows site administrators to see, where there visitors are
        now.
    """
    template_name = 'user_tracker/visitor_list.html'

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404
        return super(VisitorsMainView, self).dispatch(*args, **kwargs)

    def get_context_data(self):
        context = super(VisitorsMainView, self).get_context_data()
        context['object_list'] = Visitor.objects.active_users()
        geodata_objects = {}
        for visitor in context['object_list']:
            geodata_objects[visitor.pk] = visitor.geoip_data_json
        context['geodata'] = json.dumps(geodata_objects)
        return context


class GeoDetailsView(SingleObjectMixin, View):
    """ Detailed info about visitor to display in popup on map page.
    """
    model = Visitor

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(GeoDetailsView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        data = json.loads(serializers.serialize("json", [self.object, ]))
        ctx = data[0]['fields']
        ctx['id'] = data[0]['pk']
        ctx['user'] = {'id': 0, 'fullname': 'Anonymous', 'url': '', }
        if self.object.user is not None:
            ctx['user'] = {
                'id': self.object.user.pk,
                'fullname': self.object.user.get_full_name(),
                'url': self.object.user.profile.get_absolute_url(), }
        return HttpResponse(json.dumps(ctx), content_type="application/json")
