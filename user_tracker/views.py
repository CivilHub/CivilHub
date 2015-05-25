# -*- coding: utf-8 -*-
import json

from django.http import Http404
from django.views.generic import TemplateView

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
