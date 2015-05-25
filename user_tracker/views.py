# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class VisitorsMainView(TemplateView):
    """
    """
    template_name = 'user_tracker/visitor_list.html'
