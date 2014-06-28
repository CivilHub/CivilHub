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
from django.db import transaction
from places_core.helpers import truncatesmart
from locations.models import Location
from blog.models import News
from models import MapPointer
import forms


class Pointer(object):
    """
    Handy class to create and manage map pointers based on content type.
    """
    def __init__(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        self.latitude = obj.latitude
        self.longitude = obj.longitude
        self.content_type = ct.pk
        if isinstance(obj, News):
            self.name = obj.title
            self.desc = truncatesmart(obj.content, 10)


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
                'type'     : str(ContentType.objects.get_for_model(l)),
            })
    for p in ps:
        try:
            url = p.content_object.get_absolute_url()
        except Exception:
            break
        pointers.append({
            'latitude'    : p.latitude,
            'longitude'   : p.longitude,
            'content_type': p.content_type.pk,
            'object_pk'   : p.object_pk,
            'url'         : p.content_object.get_absolute_url(),
            'type'        : str(p.content_type),
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


@login_required
@require_POST
@transaction.non_atomic_requests
@transaction.autocommit
def delete_pointer(request):
    """
    Delete map pointer.
    """
    pk = request.POST.get('pk')
    try:
        pointer = MapPointer.objects.get(pk=pk)
    except MapPointer.DoesNotExist as ex:
        return HttpResponse(dumps({
            'success': False,
            'message': ex,
            'level'  : 'danger',
        }))
    
    if not request.user.is_superuser:
        resp = {
            'success': False,
            'message': _('Permission required'),
            'level': 'danger',
        }
    else:
        try:
            with transaction.commit_on_success(): pointer.delete()
            resp = {
                'success': True,
                'message': _('Pointer deleted'),
                'level': 'success',
            }
        except Exception as ex:
            resp = {
                'success': False,
                'message': str(ex),
                'level': 'danger',
            }
    return HttpResponse(dumps(resp))


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
