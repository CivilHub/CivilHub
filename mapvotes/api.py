# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Marker, Vote
from .serializers import MarkerSerializer


class MarkerViewSet(viewsets.ModelViewSet):
    """ This is base viewset for adding, removing and voting for markers.
    In any situation queryset should be narrowed only to one voting.
    """
    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action()
    def vote(self, request, pk):
        obj = self.get_object()
        return Response(obj.vote(request.user))

