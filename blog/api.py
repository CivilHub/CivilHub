# -*- coding: utf-8 -*-
from django.conf import settings

from rest_framework import viewsets
from rest_framework import permissions as rest_permissions

from locations.mixins import ContentMixin
from rest.permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly, \
                              IsSuperuserOrReadOnly

from .models import News, Category
from .serializers import NewsSimpleSerializer, NewsCategorySerializer


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
