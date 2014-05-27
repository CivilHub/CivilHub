# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.contrib.contenttypes.models import ContentType
from locations.models import Location
from models import MapPointer
import forms


def index(request):
    """
    This view only displays template. Places and other markers
    are loaded via AJAX and THEN map is created.
    """
    return render_to_response('maps/index.html', {'title': _("Map")})


@require_GET
def get_pointers(request):
    """
    This view actually returns map markers to place on Google Map.
    """
    from json import dumps
    locations = []
    pointers = []
    ls = Location.objects.all()
    ps = MapPointer.objects.all()
    for l in ls:
        # Take only locations with lat and long
        if l.latitude and l.longitude:
            locations.append({
                'latitude' : l.latitude,
                'longitude': l.longitude,
                'name'     : l.name,
            })
    for p in ps:
        pointers.append({
            'latitude'    : p.latitude,
            'longitude'   : p.longitude,
            'content_type': p.content_type.pk,
            'object_pk'   : p.object_pk,
        })
    context = {
        'success'  : True,
        'locations': locations,
        'pointers' : pointers,
    }
    return HttpResponse(dumps(context))


class CreateMapPoint(CreateView):
    """
    Create new map pointer for given content element. This is static view,
    mainly for testing and users that don't have javascript enabled.
    """
    model = MapPointer
    template_name = 'maps/pointer-form.html'
    form_class = forms.MapPointerForm

    def get_context_data(self, **kwargs):
        context = super(CreateMapPoint, self).get_context_data(**kwargs)
        context['title'] = _("Create map pointer")
        return context

    def get_success_url(self):
        return redirect(reverse('maps:pointers'))
