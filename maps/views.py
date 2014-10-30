# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geoip import GeoIP
from ipware.ip import get_ip
from models import MapPointer
from helpers import filter_markers, create_clusters
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MapPointerSerializer, MapObjectSerializer, \
                          MapClusterSerializer


# API views
# ------------------------------------------------------------------------------

class MapObjectAPIViewSet(viewsets.ViewSet):
    """
    This viewset is made only for GET requests. It presents entire
    list of all map objects created by users in proper format. They
    are then used to populate main map view with map pointers.
    
    Możliwe jest wyszukiwanie konkretnych obiektów w/g ID oraz typu obiektu,
    do którego odwołuje się marker. Należy w tym celu podać w parametrach GET
    typ zawartości oraz ID obiektu, np:
    
    ```/api-maps/objects/?ct=23&pk=1```
    """
    queryset = MapPointer.objects.all()

    def list(self, request):
        ct = request.QUERY_PARAMS.get('ct')
        pk = request.QUERY_PARAMS.get('pk')
        if ct and pk:
            pointers = MapPointer.objects.filter(content_type_id=ct) \
                                         .filter(object_pk=pk)
        else:
            pointers = MapPointer.objects.all()
        serializer = MapObjectSerializer(pointers, many=True,
                                        context={'request': request})
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
    paginate_by = settings.LIST_PAGINATION_LIMIT
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MapDataViewSet(APIView):
    """
    Get all markers or clusters formatted for map. You have to provide basic
    map info to get some response, this includes:
    
    `lat` means object's latitude
    `lng` is object's position longitude
    `zoom` current map zoom level
    
    For example: ```/api-maps/map-data/?zoom=10&lat=38&lng=-120```
    
    Depending on this values, data will be fetched in properly formatted way.
    Program will try to handle areas with too many markers to join them into
    cluster groups.
    """
    http_method_names = ['get',]
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        import json
        lat  = self.request.QUERY_PARAMS.get('lat', None)
        lng  = self.request.QUERY_PARAMS.get('lng', None)
        zoom = self.request.QUERY_PARAMS.get('zoom', None)
        filters = self.request.QUERY_PARAMS.get('filters', None)
        location = self.request.QUERY_PARAMS.get('location', None)

        if lat is not None and lng is not None and zoom is not None:

            if int(zoom) >= 10:
                markers = filter_markers(lat, lng, 2.0, filters, location)
                serializer = MapPointerSerializer(markers, many=True)
                context = serializer.data

            else:
                clusters = create_clusters(lat, lng, zoom)
                serializer = MapClusterSerializer(clusters, many=True)
                context = serializer.data

        else:
            context = {'count': MapPointer.objects.count()}

        return Response(context)


# Static views
# ------------------------------------------------------------------------------

class IndexView(TemplateView):
    """
    This view only displays template. Places and other markers are loaded via 
    AJAX and THEN map is created. This view serves for 2 purposes - it shows
    main map and center it on user's position or it shows main map with some
    marker highlighted when 'show on map' option is used for some content type.
    """
    http_method_names = [u'get', u'head', u'options', u'trace']
    template_name = 'maps/index.html'

    def get_context_data(self, **kwargs):
        ct = self.kwargs.get('ct', None)
        pk = self.kwargs.get('pk', None)
        active_marker = None
        context = super(IndexView, self).get_context_data(**kwargs)

        if pk and ct:
            ctype = ContentType.objects.get(pk=ct)
            obj = ctype.get_object_for_this_type(pk=pk)
            active_marker = MapPointer.objects \
                            .filter(object_pk=obj.pk,content_type=ct)[0]
            context['active_marker'] = active_marker

        if active_marker is not None:
            position = (active_marker.longitude, active_marker.latitude,)
        else:
            position = GeoIP().coords(get_ip(self.request)) or ("21.0030", "52.1356")

        context['title'] = _("Map")
        context['content_types'] = ContentType.objects.all()
        context['position'] = {'lat': position[1], 'lng': position[0]}
        context['icons'] = ['location','idea','news','poll','discussion',]
        return context
