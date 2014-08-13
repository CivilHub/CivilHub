# -*- coding: utf-8 -*-
from django.http import HttpResponse
from json import dumps
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.contrib.gis.geoip import GeoIP
from ipware.ip import get_ip
from places_core.helpers import truncatesmart, truncatehtml
from geobase.storage import CountryJSONStorage
from locations.models import Location
from blog.models import News
from geobase.models import Country
from models import MapPointer
import forms
# REST API
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest import serializers
from .serializers import MapPointerSerializer, MapObjectSerializer


class MapObjectAPIViewSet(viewsets.ViewSet):
    """
    This viewset is made only for GET requests. It presents entire
    list of all map objects created by users in proper format. They
    are then used to populate main map view with map pointers.
    
    Możliwe jest wyszukiwanie konkretnych obiektów w/g ID oraz typu obiektu,
    do którego odwołuje się marker. Należy w tym celu podać w parametrach GET
    typ zawartości oraz ID obiektu, np:
    ?ct=23&pk=1
    """
    queryset = MapPointer.objects.all()

    def list(self, request):
        ct = request.QUERY_PARAMS.get('ct')
        pk = request.QUERY_PARAMS.get('pk')
        if ct and pk:
            pointers = MapPointer.objects.filter(content_type_id=ct).filter(object_pk=pk)
        else:
            pointers = MapPointer.objects.all()
        serializer = MapObjectSerializer(pointers, many=True)
        return Response(serializer.data)


class MapPointerAPIViewSet(viewsets.ModelViewSet):
    """
    This is entry point for simple map pointer object serializer.
    It allows users to manage map pointers related to objects that
    they have created. This functionality isn't fully implemented yet.
    For now any registered user can create and manage map pointers.
    
    TODO: only owners/admins/moderators manage map pointers
    """
    queryset = MapPointer.objects.all()
    serializer_class = MapPointerSerializer
    paginate_by = 10
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MapDataViewSet(viewsets.ViewSet):
    """
    Prosty widok który umożliwia pobieranie danych mapy z wcześniej przygotowa-
    nych plików JSON. Tym sposobem unikamy dodatkowych zapytań podczas wczyty-
    wania mapy. Cała struktura danych podzielona jest w oparciu o podstawowe
    lokalizacje, czyli państwa. Przekazanie kodu państwa jako parametru w za-
    pytaniu GET zwróci listę punktów powiązanych z danym państwem, np:
    `?code=us`
    Ten widok umożliwia tylko zapytania typu GET.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request):
        s = CountryJSONStorage()
        code = request.QUERY_PARAMS.get('code')
        if code:
            return Response(s.import_data(Country.objects.get(code=code.upper()).pk))
        return Response(s.import_data())


@require_GET
def get_pointers(request):
    """
    This view actually returns map markers to place on Google Map.
    
    DEPRECATED: w chwili obecnej korzystamy z powyższych funkcji i ta prawdo-
    podobnie nie będzie już potrzebna.
    """
    locations = []
    pointers  = []
    followed  = request.GET.get('followed')
    if followed:
        ls = request.user.profile.followed_locations()
        id_list = []
        ct = ContentType.objects.get_for_model(Location)
        for location in ls:
            id_list.append(location.pk) 
        ps = []
        for point in MapPointer.objects.all():
            if point.content_object.location.pk in id_list:
                ps.append(point)
    else:
        ls = Location.objects.all()
        ps = MapPointer.objects.all()
    for l in ls:
        # Take only locations with lat and long
        if l.latitude and l.longitude:
            locations.append({
                'lat' : l.latitude,
                'lng': l.longitude,
                'content_object': {
                    'title'    : l.name,
                    'url'      : l.get_absolute_url(),
                    'type'     : str(ContentType.objects.get_for_model(l)),
                    'desc'     : truncatehtml(l.description, 100),
                    'date'     : '',
                    'img'      : l.image.url,
                    'user': l.creator.get_full_name(),
                    'profile': l.creator.profile.get_absolute_url(),
                }
            })
    for p in ps:
        pointers.append(MapObjecSerializer(p).data)
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
    
    TODO: this could be made simpler with REST framework.
    """
    from geobase.storage import CountryJSONStorage
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
        cjs = CountryJSONStorage()
        cjs.dump_data(pointer.content_object.location.country_code, False, True)
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
    
    TODO: this could be made simpler with REST framework.
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


# Static views
# ------------------------------------------------------------------------------

def index(request):
    """
    This view only displays template. Places and other markers
    are loaded via AJAX and THEN map is created.
    """
    from geobase.storage import country_codes
    code = GeoIP().country_code(get_ip(request)) or settings.DEFAULT_COUNTRY_CODE
    try:
        country = Country.objects.get(code=code)
    except Country.DoesNotExist:
        country = Country.objects.get(code=settings.DEFAULT_COUNTRY_CODE)
    return render_to_response('maps/index.html', {
        'title': _("Map"),
        'user': request.user,
        'latitude': country.latitude,
        'longitude': country.longitude,
        'zoom': country.zoom,
        'code': code,
        'content_types': ContentType.objects.all(),
        'countries': Country.objects.all(),
    })


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
