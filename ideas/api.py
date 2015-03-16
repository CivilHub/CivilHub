# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets
from rest_framework.views import APIView

from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly, IsSuperuserOrReadOnly

from .models import Category, Idea, Vote
from .serializers import IdeaSimpleSerializer, IdeaVoteSerializer, IdeaCategorySerializer


class IdeaCategoryAPIViewSet(viewsets.ModelViewSet):
    """ """
    queryset = Category.objects.all()
    serializer_class = IdeaCategorySerializer
    paginate_by = None
    permission_classes = (IsSuperuserOrReadOnly,)


class IdeaAPIViewSet(viewsets.ModelViewSet):
    """
    Zarządzanie listą pomysłów. Domyślnie widok prezentuje listę wszystkich
    pomysłów.
    
    Tworzenie idei (pola wymagane):
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


class IdeaVoteAPIViewSet(viewsets.ModelViewSet):
    """
    Widok dla głosów na idee. Domyślnie prezentuje listę wszystkich głosów.
    Możliwe jest filtrowanie wyników na podstawie ID użytkownika oraz ID idei,
    poprzez wprowadzenie odpowiednich parametrów w zapytaniu, np.:
    
        `/api-ideas/votes/?user=1&idea=3`
    
    Tworzenie idei (pola obowiązkowe):
        user (int)     pk użytkownika
        idea (int)     pk idei
        vote (boolean) Vote up/down
        
    Widok nie obsługuje paginacji.
    """
    model = Vote
    paginate_by = None
    serializer_class = IdeaVoteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,)

    def get_queryset(self):
        queryset = Vote.objects.all()
        user = self.request.QUERY_PARAMS.get('user')
        idea = self.request.QUERY_PARAMS.get('idea')
        try:
            if idea:
                queryset = queryset.filter(idea=Idea.objects.get(pk=idea))
            if user:
                queryset = queryset.filter(user=User.objects.get(pk=user))
        except Exception:
            queryset = []
        return queryset
