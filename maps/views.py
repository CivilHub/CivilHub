# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response


def index(request):
    context = {'title': _("Google maps")}
    return render_to_response('maps/index.html', context)
