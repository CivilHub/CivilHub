# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions as rest_permissions

from locations.mixins import ContentMixin
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly, \
                              IsSuperuserOrReadOnly

from .models import News, Category
from .serializers import NewsSimpleSerializer, NewsDetailedSerializer, \
                         NewsCategorySerializer


class NewsAPIView(ContentMixin):
    """ Simple view for mobile applications. Provides a way to manage blog. """
    model = News
    serializer_class = NewsSimpleSerializer
    paginate_by = settings.PAGE_PAGINATION_LIMIT
    permission_classes = (rest_permissions.IsAuthenticatedOrReadOnly,
                          IsModeratorOrReadOnly,
                          IsOwnerOrReadOnly,)


class BlogCategoryAPIViewSet(viewsets.ModelViewSet):
    """ """
    queryset = Category.objects.all()
    serializer_class = NewsCategorySerializer
    paginate_by = None
    permission_classes = (IsSuperuserOrReadOnly,)


class HotNewsBox(viewsets.ReadOnlyModelViewSet):
    """
    Show last 'hot news'. We may pass `uid` to get contents related to user or
    `lid` to get contents related to location with given ID. Returns 10 last items.
    TODO: this should be items selected by visit count.
    """
    model = News
    serializer_class = NewsDetailedSerializer
    paginate_by = None

    def get_queryset(self):
        qs = super(HotNewsBox, self).get_queryset()
        uid = self.request.QUERY_PARAMS.get('uid')
        lid = self.request.QUERY_PARAMS.get('lid')
        if uid is not None:
            user = get_object_or_404(User, pk=uid)
            qs = qs.filter(location__in=user.profile.followed_locations())
        elif lid is not None:
            qs = qs.filter(location__id=int(lid))
        return qs.order_by('-date_created')[:10]
