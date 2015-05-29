# -*- coding: utf-8 -*-
import urllib2

from rest_framework import permissions, views
from rest_framework.response import Response

from .models import MapPointer
from .storage import filter_markers, get_clusters
from .serializers import MapClusterSerializer, \
                         MapObjectSerializer, \
                         MapSimpleSeraializer


ZOOM = 9 # Zoom to switch markers/clusters


class MapObjectViewSet(views.APIView):
    """ Get map markers for selected lat/lng range. Depending on given zoom
        level this view will return different objects. On low levels (by default
        9) single markers will be returned. On lower levels we create clusters
        of appropriate size - either for regions or entire countries.
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, **kwargs):
        ne = request.QUERY_PARAMS.get('ne', '0.0x0.0')
        sw = request.QUERY_PARAMS.get('sw', '0.0x0.0')
        zoom = int(request.QUERY_PARAMS.get('zoom', ZOOM))

        # Create cluster when zoom level is not high enough
        if zoom < ZOOM:
            clusters = get_clusters(sw, ne)
            serializer = MapClusterSerializer(clusters, many=True)
            return Response(serializer.data)

        # Show single marker objects and allow for js clustering
        markers = filter_markers(sw, ne)
        filters = urllib2.unquote(request.QUERY_PARAMS.get('filters'))

        # Narrow results to selected content types only
        if filters:
            filters = [int(x.strip()) for x in filters.split(',')]
            markers = markers.filter(content_type__pk__in=filters)

        serializer = MapSimpleSeraializer(markers, many=True,
                                context={'request': request, })
        return Response(serializer.data)
