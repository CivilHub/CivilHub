# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from rest.permissions import IsOwnerOrReadOnly, \
                             IsModeratorOrReadOnly, \
                             IsSuperuserOrReadOnly

from .models import Category, Idea, Vote
from .serializers import IdeaSimpleSerializer, \
                         IdeaVoteSerializer, \
                         IdeaCategorySerializer


class IdeaCategoryAPIViewSet(viewsets.ModelViewSet):
    """ """
    queryset = Category.objects.all()
    serializer_class = IdeaCategorySerializer
    paginate_by = None
    permission_classes = (IsSuperuserOrReadOnly,)


class IdeaAPIViewSet(viewsets.ModelViewSet):
    """
    Managing the list with ideas. By default the view presents a list of all ideas.

    Creation of idea (required fields):
        name        string, max_length=64
        description string/html, max_length=20480
        location    int, Location object pk
    """
    model = Idea
    serializer_class = IdeaSimpleSerializer
    paginate_by = 5
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        obj.creator = self.request.user


class IdeaVoteAPI(APIView):
    """
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, **kwargs):
        return Response({'message': _('Revoke'), })
