# -*- coding: utf-8 -*-
from django.http import HttpResponse
from json import dumps
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
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
    return render_to_response('maps/index.html', {
        'title': _("Map"),
        'user': request.user,
    })


@require_GET
def get_pointers(request):
    """
    This view actually returns map markers to place on Google Map.
    """
    locations = []
    pointers  = []
    ls = Location.objects.all()
    ps = MapPointer.objects.all()
    for l in ls:
        # Take only locations with lat and long
        if l.latitude and l.longitude:
            locations.append({
                'latitude' : l.latitude,
                'longitude': l.longitude,
                'name'     : l.name,
                'url'      : l.get_absolute_url(),
            })
    for p in ps:
        pointers.append({
            'latitude'    : p.latitude,
            'longitude'   : p.longitude,
            'content_type': p.content_type.pk,
            'object_pk'   : p.object_pk,
            'url'         : p.content_object.get_absolute_url(),
        })
    context = {
        'success'  : True,
        'locations': locations,
        'pointers' : pointers,
    }
    return HttpResponse(dumps(context))


@login_required
@require_POST
def save_pointer(request):
    """
    This view handle ajaxy form in modal to create new map marker.
    """
    ct = ContentType.objects.get(pk=request.POST.get('content_type'))
    pointer = MapPointer()
    pointer.object_pk = request.POST.get('object_pk')
    pointer.content_type = ct
    pointer.latitude = request.POST.get('latitude')
    pointer.longitude = request.POST.get('longitude')
    try:
        pointer.save()
        context = {
            'success': True,
            'message': "Pointer added",
            'level'  : 'success',
        }
    except Exception as ex:
        context = {
            'success': False,
            'message': ex,
            'level'  : 'danger',
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
        return redirect(reverse('maps:index'))
